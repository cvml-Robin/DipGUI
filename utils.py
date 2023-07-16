import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def check_input_(tool=None,
                 default_val=0.0,
                 min_val=0.0,
                 max_val=1.0,
                 f_d=int,
                 digit=0):
    now_text = tool.text()
    try:
        now_val = float(now_text)
    except:
        now_val = default_val
    now_val = np.maximum(np.minimum(now_val, max_val), min_val)
    now_val = f_d(np.round(now_val, digit))
    tool.setText(str(now_val))
    return now_val


def window_global_style_str(
        font_size=16,
        font_name='Calibri',
        font_weight='bold'
):
    style_str = 'font-size:%dpt;font-family:%s;font-weight:%s' % (
        font_size,
        font_name,
        font_weight
    )
    return style_str

