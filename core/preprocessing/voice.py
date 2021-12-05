import noisereduce as nr


def remove_noise(data, rate):
    return nr.reduce_noise(y=data,
                           sr=rate,
                           thresh_n_mult_nonstationary=2,
                           stationary=False)
