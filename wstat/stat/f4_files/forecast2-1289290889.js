var count_word_cur = 4096;

function processWords(el) {

    var cw = getElement('counter-words');
    cw.innerHTML = count_word_cur - el.value.length;

    if ((count_word_cur - el.value.length) > 0) {
        cw.className = 'counter';
    } else {
        cw.className = 'overflow';
    }
}

function add_phrase(params)
{   
    if (is_process) {
        return;
    }

    var phrase_text = '';
    var rub_text;
    var idx;
    if (params.update_phrase) { // edit one phrase
        idx = params.idx;
        if (params.new_phrase) {
            phrase_text = params.new_phrase; // for save specify phrase
        } else {
            phrase_text = getElement('ph_' + idx).value; // save new edit box
        }
        if (phrase_text.length == 0) {
            alert(iget("Фраза не задана"));
            return;
        }

    } else if (params.update_all) { // change geo
        var all_phrases = new Array;
        var all_rub = new Array;
        for (var row = 0; row < phrases.length; row++) {
            if (phrases[row].category_url) {
                all_rub.push(phrases[row].phrase)
            } else {
                all_phrases.push(phrases[row].phrase);
            }
        }
        phrase_text = all_phrases.join(',');
        rub_text = all_rub.join(',');

    } else if (params.new_phrases) { // added new phrases from textarea
        phrase_text = getElement('ad-words').value;
        getElement('ad-words').value = '';
        if(y5) y5.Events.notify('change', getElement('ad-words'));

        rub_text = getElement('id_ChoosedCategories').value;
        rubrics_clear();

        if (phrase_text.length == 0 && rub_text.length == 0) {
            alert(iget("Фразы и рубрики не заданы"));
            return
        }
    }

    // get phrases stat by ajax ............................................
    var ajax = new AjaxObject();
    ajax.onreadycontent = function() {
        var new_phrases;
        try {
            new_phrases = eval('(' + this.responseText + ')');
        }
        catch (e) {
            document.location = SCRIPT + "?cmd=ForecastByWords";
            return;
        }

        // on error
        if (new_phrases.error) {
            if (params.update_phrase) {
                alert(new_phrases.error);
                getStyle('div1_' + idx).display = 'none';
                getStyle('div2_' + idx).display = '';
                getStyle('div3_' + idx).display = 'none';
                getStyle('action_links_' + idx).display = 'none';
                getElement('ph_' + idx).value = phrase_text;
                getElement('ph_' + idx).focus();
            } else {
                var table = getElement('result_table');
                table.deleteRow(table.rows.length - 2);
                getElement('ad-words').value = phrase_text;
                getElement('ad-words').focus();
                alert(new_phrases.error);
            }
            is_process = false;
            return;
        }

        // tag old phrases
        var md5_to_idx = new Object;
        for (var i = 0; i < phrases.length; i++) {
            phrases[i].this_is_old = true;
            md5_to_idx[phrases[i].md5] = i;
        }

        var new_phrases_hash = new Object;
        if (params.update_phrase) {
            var tmp_delete_flag = 1;
            var old_position = phrases[idx].pos;
            for (var i = 0; i < new_phrases.length; i++) {
                new_phrases[i].pos = old_position;
                new_phrases[i].enable = true;
                phrases.splice(idx, tmp_delete_flag, new_phrases[i]);
                new_phrases_hash[new_phrases[i].md5] = true;
                tmp_delete_flag = 0;
            }
        } else {
            for (var i = 0; i < new_phrases.length; i++) {
                var i_in_old_phrases = md5_to_idx[new_phrases[i].md5];
                if (params.update_all && i_in_old_phrases >= 0) {
                    new_phrases[i].pos = phrases[i_in_old_phrases].pos;
                    new_phrases[i].enable = phrases[i_in_old_phrases].enable;
                    phrases[i_in_old_phrases] = new_phrases[i];
                } else {
                    new_phrases[i].pos = 2;
                    if (new_phrases[i].fp_ctr < 0.5) {
                        new_phrases[i].enable = false;
                    } else {
                        new_phrases[i].enable = true;
                    }
                    phrases.push(new_phrases[i]);
                }
                new_phrases_hash[new_phrases[i].md5] = true;
            }
        }

        // delete dublicates
        for (var i = phrases.length - 1; i >= 0; i--) {
            if (phrases[i].this_is_old && new_phrases_hash[phrases[i].md5]) {
                phrases.splice(i, 1);
            }
        }
        
        draw(); // redraw
        clear_sort_signs();
        reverse = true;
        is_process = false;
    }

    ajax.onerrorstate = function() {
        document.location = SCRIPT + "?cmd=ForecastByWords";
        return;
    }

    is_process = true;
    if (params.update_phrase)
        getStyle('div3_' + idx).display = ''
    else
        insert_table_wait_row();

    var phrases_url = phrase_text && phrase_text.length ? "&phrases=" + encodeURIComponent(phrase_text) : '';
    var choosed_categories_url = rub_text ? '&ChoosedCategories=' + encodeURIComponent(rub_text) : '';
    var force_advq_url = params.force_advq  ? "&force_advq="+encodeURIComponent(params.force_advq) : '';
    var geo = encodeURIComponent($('#geo').val());
    var currency_url = "&pseudo_currency_id="+encodeURIComponent(pseudo_currency_id);
    ajax.open('POST', SCRIPT);

    ajax.send("cmd=calcForecast&ajax=1&no_auto_catalog=1"
               + "&geo=" + geo
               + choosed_categories_url
               + phrases_url
               + force_advq_url
               + currency_url
               );

    return true;
}

function draw()
{
    // sort phrases - rubrics after phrases
    var rub_tmp = new Array;
    var phr_tmp = new Array;

    for (var i = 0; i < phrases.length; i++) {
        if (phrases[i].category_url) {
            rub_tmp.push(phrases[i]);
        } else {
            phr_tmp.push(phrases[i]);
        }
    }
    phrases = phr_tmp.concat(rub_tmp);

    var table = getElement('result_table');

    // clear global _main.js::elements_cache
    elements_cache = new Object();
    // clear
    while (table.rows.length > 2) {
        table.deleteRow(1);
    }

    // rendering
    var first_only = true;
    for (var row = 0; row < phrases.length; row++) {
        if (first_only && phrases[row].category_url) {
            insert_table_row_br(table);
            first_only = false;
        }
        insert_table_row(table, row, phrases[row]);
    }

    recalc();
}

function insert_table_row_br(table)
{
    var tr = table.insertRow(table.rows.length - 1);

    var td, div;

    td = tr.insertCell(-1);
    td.colSpan = 10;
    td.style.height = '1px';
    td.style.padding = '0';
    td.style.margin = '0';
    td.style.overflow = 'hidden';
    tr.style.height = '1px';
    tr.style.overflow = 'hidden';
    td.style.background = '#e3dee9';
    div = document.createElement('div');
    div.style.height = '1px';
    div.style.fontSize = '1px';
    div.style.overflow = 'hidden';
    td.appendChild(div);
}

function insert_table_row(table, row, phrase)
{
    var tr = table.insertRow(table.rows.length - 1);
    tr.className = 'tdata old-tr-top';
    tr.id = 'tr' + row;
    tr.style.color = phrase.enable ? 'black' : 'gray';
    var td, div;

    // icon for delete phrase
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = "<a href='#' onClick='delete_phrase(" + row + "); return false;'><img src='/i/i-delete.gif' width='13' height='13' border='0' alt='" + iget("удалить фразу") + "' title='" + iget("удалить фразу") + "'></a>";
    div.className = "hide_this_for_print";
    td.appendChild(div);

    // checkbox for disable
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = "<input type='checkbox' class='tcheck' id='enable_" + row + "' onClick='return change_enable(" + row + ")' tabindex='1'>";
    div.className = "hide_this_for_print";
    td.appendChild(div);
    getElement('enable_' + row).checked = phrase.enable ? true : false;
    getElement('enable_' + row).title = phrase.enable ? iget("не учитывать в расчете") : iget("учитывать в расчете");

    // phrase
    td = tr.insertCell(-1);
    div = document.createElement('div');
    var phrase_or_rub_link, phrase_text;
    if (phrase.category_url) {
        phrase_or_rub_link = iget("Рубрика:") + ' <a href="' + phrase.category_url + '" target=_blank>' + phrase.category_name + '</a>';
        phrase_text = iget("Рубрика:") + phrase.category_name;
    } else {
        var tmp_phr = phrase.phrase.replace(/^(.{90,120}\S\s+).+$/, '$1&nbsp;...');
        var phr_without_minus = phrase.phrase.replace(/\s+-.+$/, '');
        phrase_or_rub_link = "<em><a href='/registered/prices.pl?cmd=get&req=" + encodeURIComponent(phr_without_minus) + "' onclick='OpenWindow(this.href,700,600); return false;'>" + tmp_phr + "</a></em>";
        phrase_text = "<em>" + tmp_phr + "</em>";
    }
    if (phrase.fp_ctr < 0.5) {
        var help_link = ' <a href="/help/text.xml?id=995285" onClick="OpenWindow(this.href, 700, 600); return false;" ><img title="'
                        + iget("Прогноз CTR ниже допустимого значения")
                        + '" alt="'
                        + iget("Прогноз CTR ниже допустимого значения")
                        + '" width="10" height="10" border="0" src="/i/i-help.gif" style="position:relative;top:1px;"></a>';
        phrase_or_rub_link += help_link;
        phrase_text += help_link;
    }
    var display_phrase_link, display_phrase_div;
    if (phrase.enable) {
        display_phrase_link = "";
        display_phrase_div = "style='display: none;'"
    } else {
        display_phrase_link = "style='display: none;'";
        display_phrase_div = ""
    }
    div.innerHTML = "<div id='div1_" + row + "' " + display_phrase_link + ">" + phrase_or_rub_link + "</div>"
                  + "<div id='div2_" + row + "' style='display: none; white-space: nowrap; width: 100%;'>"
                    + "<input type='text' id='ph_" + row + "' onBlur='edit_phrase(event, " + row + ", 1);' onKeyPress='phrase_press_key(event, " + row + ")' style='width: 85%' tabindex='1'>"
                    + "<input type='button' value='ok'>"
                  + "</div>"
                  + "<div id='div3_" + row + "' style='display: none;' class='wait_bar'></div>"
                  + "<div id='div4_" + row + "' " + display_phrase_div + ">" + phrase_text + "</div>";
    div.className = 'my_div';
    td.appendChild(div);

    // action link
    td = tr.insertCell(-1);
    div = document.createElement('span');
    div.innerHTML = (phrase.category_url ? "&nbsp;" :
                      "<label><a id='ahref_" + row + "' href='#' class='tlink' onClick='edit_phrase(event, " + row + "); return false;'>" + iget("изменить") + "</a></label><br/>" + add_additional_actions(row)
                    );
    div.className = 'hide_this_for_print';
    div.id = 'action_links_' + row;
    div.style.display = phrase.enable ? '' : 'none';
    td.appendChild(div);
    td.appendChild(document.createTextNode("\u00a0"));

    // position labels
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = "<label for='rb1_" + row + "'>" + iget("спецразмещение") + "</label><br/>"
                  + "<label for='rb2_" + row + "'>" + iget("1-ое местo") + "</label><br/>"
                  + "<label for='rb3_" + row + "'>" + iget("гарантированные показы") + "</label>";
    td.noWrap = true;
    td.appendChild(div);

    // prices
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = "<label id='price_text1_" + row + "' for='rb1_" + row + "'>" + round2s(phrase.pmin) + "</label><br/>"
                  + "<label id='price_text2_" + row + "' for='rb2_" + row + "'>" + round2s(phrase.max)  + "</label><br/>"
                  + "<label id='price_text3_" + row + "' for='rb3_" + row + "'>" + round2s(phrase.min)  + "</label>";
    td.noWrap = true;
    td.align = 'right';
    td.className = 'old-td-right';
    td.appendChild(div);
    getStyle('price_text' + phrase.pos + '_' + row).fontWeight = 'bold';

    // position radio-buttons
    td = tr.insertCell(-1);
    div = document.createElement('div');
    var radio_disabled = phrase.enable ? '' : 'disabled="disabled"';
    div.innerHTML = " <input type='radio' id='rb1_" + row + "' name='rb_" + row + "' class='radio_inputs' onClick='on_change_pos(" + row + ", 1)' tabindex='1' " + radio_disabled + "><br/>"
                  + " <input type='radio' id='rb2_" + row + "' name='rb_" + row + "' class='radio_inputs' onClick='on_change_pos(" + row + ", 2)' tabindex='1' " + radio_disabled + "><br/>"
                  + " <input type='radio' id='rb3_" + row + "' name='rb_" + row + "' class='radio_inputs' onClick='on_change_pos(" + row + ", 3)' tabindex='1' " + radio_disabled + ">";
    td.noWrap = true;
    td.align = 'right';
    td.className = 'old-td-right';
    td.appendChild(div);
    getElement('rb' + phrase.pos + '_' + row).checked = true;

    // ctr
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = "<label id='ctr_text1_" + row + "' for='rb1_" + row + "'>" + round2s(phrase.p_ctr)  + "</label><br/>"
                  + "<label id='ctr_text2_" + row + "' for='rb2_" + row + "'>" + round2s(phrase.fp_ctr) + "</label><br/>"
                  + "<label id='ctr_text3_" + row + "' for='rb3_" + row + "'>" + round2s(phrase.ctr) + "</label>";
    td.noWrap = true;
    td.align = 'right';
    td.className = 'old-td-right';
    td.appendChild(div);
    getStyle('ctr_text' + phrase.pos + '_' + row).fontWeight = 'bold';

    // shows
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML = '<label>' + phrase.shows + '</label>';
    td.noWrap = true;
    td.align = 'right';
    td.className = 'old-td-right';
    td.appendChild(div);

    if (show_clicks_column) {
        // clicks
        td = tr.insertCell(-1);
        div = document.createElement('div');
        div.innerHTML = "<label for='rb1_" + row + "'>" + phrase.p_clicks  + "</label><br/>"
                      + "<label for='rb2_" + row + "'>" + phrase.fp_clicks + "</label><br/>"
                      + "<label for='rb3_" + row + "'>" + phrase.clicks + "</label>";
        td.noWrap = true;
        td.align = 'right';
        td.className = 'old-td-right'
        td.appendChild(div);
    }

    // sum
    td = tr.insertCell(-1);
    div = document.createElement('div');
    div.innerHTML =  "<label for='rb1_" + row + "'><span id='sum_text1_" + row + "'>" + phrase.p_sum.toFixed(2) + "</span></label><br/>"
                   + "<label for='rb2_" + row + "'><span id='sum_text2_" + row + "'>" + phrase.fp_sum.toFixed(2) + "</span></label><br/>"
                   + "<label for='rb3_" + row + "'><span id='sum_text3_" + row + "'>" + phrase.sum.toFixed(2) + "</span></label>";
    td.noWrap = true;
    td.align = 'right';
    td.className = 'old-td-right';
    td.appendChild(div);
    getStyle('sum_text' + phrase.pos + '_' + row).fontWeight = 'bold';
}

function insert_table_wait_row()
{
    var table = getElement('result_table');

    var tr = table.insertRow(table.rows.length - 1);
    tr.className = 'tdata old-tr-top';

    var td = tr.insertCell(-1);
    td.colSpan = 10;
    td.align = 'center';
    td.innerHTML = "<img src='/i/wait-big.gif'>";

    // set gray background
    for (var i = 1; i < table.rows.length - 2; i++) {
        table.rows[i].style.backgroundColor = '#f4f4f4';
    }
}

function insert_table_empty_row()
{
    var table = getElement('result_table');

    var tr = table.insertRow(table.rows.length - 1);
    tr.className = 'tdata old-tr-top';

    var td = tr.insertCell(-1);
    td.colSpan = 2;
    td.align = 'left';
    td.innerHTML = "&nbsp;";
    td = tr.insertCell(-1);
    td.colSpan = 10;
    td.align = 'left';
    td.innerHTML = "<div class='my_div'>" + iget("Слова не выбраны") + "</div>";

    getStyle('message_phrases_present').display = 'none';
    getStyle('message_phrases_not_present').display = 'none';
    getStyle('message_phrases_sum_text').display = 'none';
    getStyle('message_phrases_nosum_text').display = 'none';
}

function recalc()
{
    var total_sum = 0;
    var total_sum_p = 0;
    var total_sum_fp = 0;
    var total_sum_gar = 0;
    var total_shows = 0;
    var enable_all = true;
    var disable_all = true;

    for (var row = 0; row < phrases.length; row++) {
        var phrase = phrases[row];
        if (! phrase.enable) {
            enable_all = false;
            continue;
        }
        if (phrase.enable) {
            disable_all = false;
        }
        var sum = [phrase.p_sum, phrase.fp_sum, phrase.sum][phrase.pos - 1];
        total_sum     += sum;
        total_sum_p   += phrase.p_sum;
        total_sum_fp  += phrase.fp_sum;
        total_sum_gar += phrase.sum;
        total_shows   += phrase.shows;
    }

    getElement('cb_enable_all').checked = enable_all;
    getElement('cb_enable_all').title = enable_all ? iget("не учитывать в расчете все фразы") : iget("учитывать в расчете все фразы");

    getElement('total_sum').innerHTML = total_sum.toFixed(2);
    getElement('total_sum_rub').innerHTML = (total_sum * currency_rate).toFixed(0);

    if (show_additional_sums) {
      getElement('total_sum_rub2').innerHTML    = (total_sum * currency_rate).toFixed(0);
      getElement('total_sum_rub_p').innerHTML   = (total_sum_p * currency_rate).toFixed(0);
      getElement('total_sum_rub_fp').innerHTML  = (total_sum_fp * currency_rate).toFixed(0);
      getElement('total_sum_rub_gar').innerHTML = (total_sum_gar * currency_rate).toFixed(0);
    }

    getElement('total_shows').innerHTML = total_shows;

    if (total_sum > 0 ) {
        getStyle('message_phrases_sum_text').display = '';
        getStyle('message_phrases_nosum_text').display = 'none';
    } else {
        getStyle('message_phrases_nosum_text').display = '';
        getStyle('message_phrases_sum_text').display = 'none';
    }

    if (disable_all) {
        getStyle('message_phrases_present').display = 'none';
        getStyle('message_phrases_not_present').display = '';
    } else {
        getStyle('message_phrases_present').display = '';
        getStyle('message_phrases_not_present').display = 'none';
    }

    if (phrases.length == 0) {
        getStyle('cb_enable_all').display = 'none';
        getStyle('img_enable_all').display = 'none';
        getStyle('message_phrases_present').display = 'none';
        getStyle('message_phrases_present2').display = 'none';
        clear_sort_signs();
    } else {
        getStyle('cb_enable_all').display = '';
        getStyle('img_enable_all').display = '';
        getStyle('message_phrases_present2').display = '';
    }

    show_phrases_list(true);
}

function edit_phrase(event, idx, is_blur)
{
    if (getStyle('div1_' + idx).display == '') {

        if (is_blur) {
            return;
        }

        // edit
        getStyle('div1_' + idx).display = 'none';
        getStyle('div2_' + idx).display = '';
        getStyle('action_links_' + idx).display = 'none';
        getElement('ph_' + idx).value = phrases[idx].phrase;
        getElement('ph_' + idx).focus();

    } else {

        if (getElement('ph_' + idx).value.length == 0) {
            getElement('ph_' + idx).blur();
            alert(iget("Фраза не задана"));
            getElement('ph_' + idx).focus();
            return;
        }

        // save
        if (phrases[idx].phrase != getElement('ph_' + idx).value) {
            getStyle('div3_' + idx).display = '';
            add_phrase({update_phrase: true, idx: idx, force_advq: get_selected_advq()});
        } else {
            getStyle('div1_' + idx).display = '';

            // IE hack for lost focus
            getElement('div2_' + idx).removeChild(getElement('div2_' + idx).lastChild);
            var inp = document.createElement('input');
            inp.type = 'button';
            inp.value = 'ok';
            getElement('div2_' + idx).appendChild(inp);
        }

        getStyle('action_links_' + idx).display = '';
        getStyle('div2_' + idx).display = 'none';
    }
}

function phrase_press_key(event, idx)
{
    if (event.keyCode == 13)
    {
        getElement('ph_' + idx).blur();

        if (getElement('ph_' + idx).value.length == 0) {
            getElement('ph_' + idx).blur();
            alert(iget("Фраза не задана"));
            getElement('ph_' + idx).focus();
            return;
        }

        // save
        if (phrases[idx].phrase != getElement('ph_' + idx).value) {
            getStyle('div3_' + idx).display = '';
            add_phrase({update_phrase: true, idx: idx, force_advq: get_selected_advq()});
        } else {
            getStyle('div1_' + idx).display = '';
            getStyle('div2_' + idx).display = 'none';
            getElement('ph_' + idx).blur();
        }

        getStyle('action_links_' + idx).display = '';
        getStyle('div2_' + idx).display = 'none';
    }
}

function delete_phrase(idx)
{
    if (is_process)
        return;

    var phrase_or_rub = phrases[idx].category_url ? iget("рубрику") : iget("фразу");
    if (! confirm(iget("Вы желаете удалить") + ' ' + phrase_or_rub + '?')) {
        return;
    }

    phrases.splice(idx, 1);
    draw();

    if (phrases.length == 0) {
        insert_table_empty_row();
    }
}

function delete_all_phrases()
{
    if (is_process)
        return;

    if (! confirm(iget("Вы желаете удалить все фразы?"))) {
        return;
    }

    phrases = new Array;
    draw();
    insert_table_empty_row();
}

// change pos ..............................................................
function on_change_pos(idx, pos)
{
    mark_bold_position(idx, pos);

    if (cur_sort_column != 'phrase' && cur_sort_column != 'shows') {
        clear_sort_signs();
    }

    recalc();
}

function set_mass_position(pos)
{
    if (phrases.length == 0 || is_process || is_print_page) {
        return;
    }

    for (var row = 0; row < phrases.length; row++) {
        getElement('rb' + pos + '_' + row).checked = true;
        mark_bold_position(row, pos);
    }

    if (cur_sort_column != 'phrase' && cur_sort_column != 'shows') {
        clear_sort_signs();
    }

    recalc();
}

function mark_bold_position(idx, new_pos)
{
    var prefix = ['price', 'ctr', 'sum'];
    var old_pos = phrases[idx].pos;
    phrases[idx].pos = new_pos;

    for (var k = 0; k < prefix.length; k++) {
        getStyle(prefix[k] + '_text' + old_pos + '_' + idx).fontWeight = '';
        getStyle(prefix[k] + '_text' + new_pos + '_' + idx).fontWeight = 'bold';
    }
}

// enable ..................................................................
function change_enable(idx, force, not_calc)
{
    if (is_process && ! force) {
        return false;
    }

    phrases[idx].enable = getElement('enable_' + idx).checked;
    if (phrases[idx].enable) {
        getElement('tr' + idx).style.color = 'black';

        getElement('rb1_' + idx).disabled = false;
        getElement('rb2_' + idx).disabled = false;
        getElement('rb3_' + idx).disabled = false;

        getStyle('div1_' + idx).display = '';
        getStyle('div2_' + idx).display = 'none';
        getStyle('div3_' + idx).display = 'none';
        getStyle('div4_' + idx).display = 'none';

        getStyle('action_links_' + idx).display = '';

    } else {
        getElement('tr' + idx).style.color = 'gray';

        getElement('rb1_' + idx).disabled = true;
        getElement('rb2_' + idx).disabled = true;
        getElement('rb3_' + idx).disabled = true;

        getStyle('div1_' + idx).display = 'none';
        getStyle('div2_' + idx).display = 'none';
        getStyle('div3_' + idx).display = 'none';
        getStyle('div4_' + idx).display = '';

        getStyle('action_links_' + idx).display = 'none';
    }

    if (! not_calc) {
        recalc();
    }

    getElement('enable_' + idx).title = phrases[idx].enable ? iget("не учитывать в расчете") : iget("учитывать в расчете");

    return true;
}

function change_enable_all()
{
    if (is_process)
        return;

    var checked = getElement('cb_enable_all').checked;
    for (var row = 0; row < phrases.length; row++) {
        phrases[row].enable = checked;
        getElement('enable_' + row).checked = checked;
        change_enable(row, false, true);
    }
    recalc();
}

// sorting .................................................................
var reverse = false;
var cur_sort_column;

function sort_table(column)
{
    if (phrases.length == 0 || is_process || is_print_page) {
        return;
    }

    if (cur_sort_column == column) {
        reverse = ! reverse;
    } else {
        reverse = false;
    }
    cur_sort_column = column;

    clear_sort_signs();
    if (reverse) {
        getElement('sort_sign_' + column).innerHTML = '&nbsp;&#x25BC;';
    } else {
        getElement('sort_sign_' + column).innerHTML = '&nbsp;&#x25B2;';
    }
    getStyle('sort_sign_' + column).color = '#707070';
    sort_phrases_array(column, reverse);
    draw();
}

function sort_phrases_array(column, reverse)
{
    phrases.sort(function (a, b) {

        var aa, bb;

        if (column == 'phrase') {
            aa = ! a.category_url ? 'a' + a.phrase.toLowerCase() : 'z' + a.category_name.toLowerCase();
            bb = ! b.category_url ? 'a' + b.phrase.toLowerCase() : 'z' + b.category_name.toLowerCase();
        } else if (column == 'pos') {
            aa = b.pos;
            bb = a.pos;
        } else if (column == 'price') {
            aa = [a.pmin, a.max, a.min][a.pos - 1];
            bb = [b.pmin, b.max, b.min][b.pos - 1];
        } else if (column == 'ctr') {
            aa = [a.p_ctr, a.fp_ctr, a.ctr][a.pos - 1];
            bb = [b.p_ctr, b.fp_ctr, b.ctr][b.pos - 1];
        } else if (column == 'shows') {
            aa = a.shows;
            bb = b.shows;
        } else if (column == 'sum') {
            aa = [a.p_sum, a.fp_sum, a.sum][a.pos - 1];
            bb = [b.p_sum, b.fp_sum, b.sum][b.pos - 1];
        } else {
            return 0;
        }

        if (aa < bb)
            return reverse ? 1 : -1;
        if (aa > bb)
            return reverse ? -1 : 1;
        return 0;
    });
}

function clear_sort_signs()
{
    var sort_columns = new Array ('phrase', 'pos', 'price', 'ctr', 'shows', 'sum');
    for (var i = 0; i < sort_columns.length; i++) {
        getStyle('sort_sign_' + sort_columns[i]).color = '#F0F1F3';
    }
}

function write_sort_column(name, caption, align)
{
    var style = '';
    if (navigator.appName.toLowerCase().indexOf('opera') != -1) {
        style = ' style="bottom:-2px;right:-9px;" ';
    }

    var str = '<div style="float: ' + align + ';position: relative"><div><a href="#" onClick="sort_table(' + "'" + name + "'" + '); return false;">' + caption + '</a></div>'
              + '<span class="sort_sign" onclick="sort_table('+ "'" + name + "'" +'); return false;" id="sort_sign_' + name + '"' + style + '>&#x25B2;</span></div>';
    document.write(str);
}

// change phrases ..........................................................
function change_geo()
{
    if (! is_step2) {
        return;
    }
    
    setTimeout(function()
               {
                   add_phrase({update_all: true, force_advq: get_selected_advq()});
               }, 50);
}

function open_wordstat()
{
    var w = 800, h = 600;
    if (document.all || document.layers) {
        w = screen.availWidth;
        h = screen.availHeight;
    }

    var popW = 700, popH = 600;
    var leftPos = (w - popW) / 2, topPos = (h - popH) / 2;
    var shw = 0;
    WordsWin2 = window.open("/registered/main.pl?checkboxes=1"
                          + "&cmd=wordstat"
                          + "&from_forecast=1"
                          + "&tm=" + time
                          + '&geo=' + encodeURIComponent(document.forms['ad'].geo.value)
                          , "Words", 'width=' + popW + ',height=' + popH + ',top=' + topPos + ',left=' + leftPos + ',resizable=yes,scrollbars=yes,status=0');
    if (navigator.appName == 'Netscape') {
        WordsWin2.focus();
    }
}

function on_submit_on_first_step()
{
    if (getElement('ad-words').value.length == 0 && getElement('id_ChoosedCategories').value.length == 0) {
        alert(iget("Фразы и рубрики не заданы"));
        return;
    }

    var phrase_text = getElement('ad-words').value;
    var ajax = new AjaxObject();
    ajax.onreadycontent = function() {

        var result;
        try {
            result = eval('(' + this.responseText + ')');
        }
        catch (e) {
            return;
        }

        // on error
        if (result.error) {
            alert(result.error);
            getElement('ad-words').focus();
            return;
        } else {
            document.forms['ad'].submit();
        }
    }

    ajax.onerrorstate = function() {
        document.forms['ad'].submit();
    }

    var phrases_url = phrase_text && phrase_text.length ? "&phrases=" + encodeURIComponent(phrase_text) : '';
    ajax.open('POST', SCRIPT);
    ajax.send("cmd=calcForecast&ajax=1&no_auto_catalog=1&validate_phrase_only=1" + phrases_url);
}

function show_phrases_list(hide)
{
    if (hide || getStyle('phrases_list_div').display == '') {
        getStyle('phrases_list_div').display = 'none';
        getElement('show_phrases_list_sign').innerHTML = '&nbsp;&#x25BA;';
    } else {
        getStyle('phrases_list_div').display = '';
        var all_phrases = new Array;
        for (var row = 0; row < phrases.length; row++) {
            if (! phrases[row].category_url && phrases[row].enable) {
                all_phrases.push(phrases[row].phrase);
            }
        }
        getElement('phrases_list_textarea').value = all_phrases.join(",\n");
        getElement('show_phrases_list_sign').innerHTML = '&nbsp;&#x25BC;';
        getElement('phrases_list_textarea').focus();
        getElement('phrases_list_textarea').select();
    }
}

function show_print_page()
{
    is_print_page = ! is_print_page;
    var display_style = is_print_page ? 'none' : '';

    var all_tags = document.getElementsByTagName("*");

    for (var i = 0; i < all_tags.length; i++) {
        try {
            if (all_tags[i].className && (all_tags[i].className == 'global-project' || all_tags[i].className.match(/hide_this_for_print/))) {
                all_tags[i].style.display = display_style;
            }
        } catch(e) {}
    }

    if (is_print_page) {
        getElement('print_version_link').innerHTML = iget("Полная версия");
    } else {
        getElement('print_version_link').innerHTML = iget("Версия для печати");
    }
}

function export_to_xls()
{
    if (phrases.length == 0) {
        alert(iget("Фразы и рубрики не заданы"));
        return;
    }

    var form = document.forms['xls'];
    form.action = 'forecast.' + Math.floor(10000 * Math.random()) + '.xls';

    // clear
    while (form.firstChild) {
        form.removeChild(form.firstChild);
    }
    // generate new form
    add_hidden_input(form, 'cmd', 'forecastXls');
    add_hidden_input(form, 'pseudo_currency_id', pseudo_currency_id);
    add_hidden_input(form, 'geo', document.forms['ad'].geo.value);
    
    var check_form = add_additional_to_xls_form(form);
    if (! check_form)
        return false;

    for (var i = 0; i < phrases.length; i++) {

        if (! phrases[i].enable) {
            continue;
        }

        add_hidden_input(form, 'phrase_' + i,        phrases[i].phrase);
        add_hidden_input(form, 'shows_' + i,         phrases[i].shows);
        add_hidden_input(form, 'clicks_' + i,        phrases[i].clicks);
        add_hidden_input(form, 'fp_clicks_' + i,     phrases[i].fp_clicks);
        add_hidden_input(form, 'p_clicks_' + i,      phrases[i].p_clicks);
        add_hidden_input(form, 'ctr_' + i,           phrases[i].ctr);
        add_hidden_input(form, 'fp_ctr_' + i,        phrases[i].fp_ctr);
        add_hidden_input(form, 'p_ctr_' + i,         phrases[i].p_ctr);
        add_hidden_input(form, 'min_' + i,           phrases[i].min);
        add_hidden_input(form, 'pmin_' + i,          phrases[i].pmin);
        add_hidden_input(form, 'max_' + i,           phrases[i].max);
        add_hidden_input(form, 'pos_' + i,           phrases[i].pos);
        add_hidden_input(form, 'category_name_' + i, phrases[i].category_name);
        add_hidden_input(form, 'category_url_' + i,  phrases[i].category_url);
        add_hidden_input(form, 'sign_' + i,          phrases[i].sign);
    }

    form.submit();
}

function add_hidden_input(form, name, value)
{
    if (value == null) {
        return;
    }

    var input = document.createElement('input');
    input.name = name;
    input.type = 'hidden';
    form.appendChild(input);
    input.value = value;
}
