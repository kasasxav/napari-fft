from magicgui import magic_factory, widgets
import napari
import numpy as np
from napari.qt import thread_worker
from concurrent.futures import Future


@magic_factory
def fft_widget(image: napari.types.ImageData) -> Future[napari.types.ImageData]:

    future: Future[napari.types.ImageData] = Future()
    pbar = widgets.ProgressBar()
    pbar.range = (0, 0)  # unknown duration
    fft_widget.insert(0, pbar)  # add progress bar to the top of widget

    def _on_done(result, self=fft_widget):
        future.set_result(result)
        self.remove(pbar)

    @thread_worker()
    def _fft():
        return np.fft.fftshift(np.log10(abs(np.fft.fft2(image))))

    worker = _fft()
    worker.returned.connect(_on_done)
    worker.start()

    return future
