# coding=utf-8


def level_style_(lv):
    style = {
        0: 'background-color:#bfbfbf; color: white',
        1: 'background-color:#bfbfbf; color: white',
        2: 'background-color:#95ddb2; color: white',
        3: 'background-color:#92d1e5; color: white',
        4: 'background-color:#ffb37c; color: white',
        5: 'background-color:#ff6c00; color: white',
        6: 'background-color:#ff0000; color: white'
    }
    return style.get(lv, "")


def button_style(name_, type_='normal', effect_='normal'):
    colors = {
        'normal': {
            'color': {'normal': '#606266', 'plain': '#606266'},
            'border': {'normal': '#dcdfe6', 'plain': '#dcdfe6'},
            'background': {'normal': '#fff', 'plain': '#fff'},
            'hoverBorder': {'normal': '#c6e2ff', 'plain': '#409eff'},
            'hoverBackground': {'normal': '#ecf5ff', 'plain': '#fff'},
        },
        'primary': {
            'color': {'normal': '#fff', 'plain': '#409eff'},
            'border': {'normal': '#409eff', 'plain': '#b3d8ff'},
            'background': {'normal': '#409eff', 'plain': '#ecf5ff'},
            'hoverBorder': {'normal': '#66b1ff', 'plain': '#409eff'},
            'hoverBackground': {'normal': '#66b1ff', 'plain': '#409eff'},
        },
        'success': {
            'color': {'normal': '#fff', 'plain': '#67c23a'},
            'border': {'normal': '#67c23a', 'plain': '#c2e7b0'},
            'background': {'normal': '#67c23a', 'plain': '#f0f9eb'},
            'hoverBorder': {'normal': '#85ce61', 'plain': '#67c23a'},
            'hoverBackground': {'normal': '#85ce61', 'plain': '#67c23a'},
        },
        'info': {
            'color': {'normal': '#fff', 'plain': '#909399'},
            'border': {'normal': '#909399', 'plain': '#d3d4d6'},
            'background': {'normal': '#909399', 'plain': '#f4f4f5'},
            'hoverBorder': {'normal': '#a6a9ad', 'plain': '#909399'},
            'hoverBackground': {'normal': '#a6a9ad', 'plain': '#909399'},
        },
        'warning': {
            'color': {'normal': '#fff', 'plain': '#e6a23c'},
            'border': {'normal': '#e6a23c', 'plain': '#f5dab1'},
            'background': {'normal': '#e6a23c', 'plain': '#fdf6ec'},
            'hoverBorder': {'normal': '#ebb563', 'plain': '#e6a23c'},
            'hoverBackground': {'normal': '#ebb563', 'plain': '#e6a23c'},
        },
        'danger': {
            'color': {'normal': '#fff', 'plain': '#f56c6c'},
            'border': {'normal': '#f56c6c', 'plain': '#fbc4c4'},
            'background': {'normal': '#f56c6c', 'plain': '#fef0f0'},
            'hoverBorder': {'normal': '#f78989', 'plain': '#f56c6c'},
            'hoverBackground': {'normal': '#f78989', 'plain': '#f56c6c'},
        }
    }
    dict_ = colors.get(type_ if type_ else 'normal')
    result = "#{} {{" \
             "   color: {};" \
             "   border: 1px solid {};" \
             "   background-color: {};" \
             "   border-radius: {};" \
             "}}" \
             "#{}:hover {{" \
             "   color: {};" \
             "   border-color: {};" \
             "   background-color: {};" \
             "}}"
    result = result.format(name_, dict_['color'].get(effect_), dict_['border'].get(effect_),
                           dict_['background'].get(effect_), '4px' if effect_ != 'round' else '20px',
                           name_, '#409eff' if type_ == 'normal' else '#fff', dict_['hoverBorder'].get(effect_),
                           dict_['hoverBackground'].get(effect_))
    return result


def border_style_(object_name):
    return '#{}{{border-color:#828790;border-style:solid;border-width:1px;}}'.format(
        object_name)


def scroll_bar_style(inline_style, background_style='background:#F5F5F5;'):
    return ('QScrollArea{{'
            '  {}'
            '  border-radius: 2px;'
            '}}'
            'QScrollBar:vertical'
            '{{'
            '  width: 8px;'
            '  border:0px solid;'
            '  border-radius: 2px;'
            '  margin: 0px,0px,0px,0px;'
            '  {}'
            '}}'
            'QScrollBar:vertical:hover'
            '{{'
            '  width: 8px;'
            '  border:0px solid;'
            '  margin: 0px,0px,0px,0px;'
            '  background: #707e88;'
            '}}'
            'QScrollBar::handle:vertical'
            '{{'
            '  width: 8px;'
            '  background: #E1E1E1;'
            '  border-radius: 2px;'
            '  height: 40px;'
            '}}'
            'QScrollBar::handle:vertical:hover'
            '{{'
            '  background: #cbcbcb;'
            '  border-radius: 2px;'
            '}}'
            'QScrollBar::up-arrow:vertical{{'
            '  image : none;'
            '  border:0px solid;'
            '  border-radius: 3px;'
            '}}'
            'QScrollBar::down-arrow:vertical {{'
            '  image : none;'
            '  border:0px solid;'
            '  border-radius: 3px;'
            '}}').format(inline_style, background_style)
