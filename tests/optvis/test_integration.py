import pytest

import torch
from lucent.optvis import objectives, param, render, transform
from lucent.modelzoo import inceptionv1


@pytest.mark.parametrize("decorrelate", [True, False])
@pytest.mark.parametrize("fft", [True, False])
def test_integration(decorrelate, fft):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = inceptionv1().to(device).eval()
    obj = "mixed3a_1x1_pre_relu_conv:0"
    param_f = lambda: param.image(224, decorrelate=decorrelate, fft=fft)
    optimizer = lambda params: torch.optim.Adam(params, lr=0.1)
    rendering = render.render_vis(
        model,
        obj,
        param_f,
        optimizer=optimizer,
        thresholds=(1, 2),
        verbose=True,
        show_inline=True,
    )
    start_image, end_image = rendering

    assert (start_image != end_image).any()
