Place this after **Section 2.4: Radar Datasets and Benchmarking Approaches**.

**Table 2.1: Comparison of the two radar application settings considered in this study**

<table>
  <tr><th>Aspect</th><th>Automotive FMCW Radar Perception</th><th>Wideband Radar Spectrum Detection</th></tr>
  <tr><td>Primary objective</td><td>Detect and localise spatial targets</td><td>Detect and classify radar emissions</td></tr>
  <tr><td>Typical input</td><td>Complex ADC data cube or Range-Doppler representation</td><td>Time-frequency spectrogram</td></tr>
  <tr><td>Main information</td><td>Range, velocity, azimuth and target characteristics</td><td>Signal dwell time, frequency occupancy and modulation</td></tr>
  <tr><td>Output</td><td>Target detections, coordinates and semantic classes</td><td>Signal bounding boxes and modulation classes</td></tr>
  <tr><td>Data considered</td><td>Synthetic 77 GHz FMCW measurements</td><td>RadDet wideband radar dataset</td></tr>
  <tr><td>Learning-based approach</td><td>Convolutional neural network</td><td>YOLO-based object detector</td></tr>
  <tr><td>Conventional processing</td><td>FFT, MTI, CFAR, MUSIC and DBSCAN</td><td>Spectrum analysis and signal detection</td></tr>
  <tr><td>Evaluation focus</td><td>Target localisation and classification</td><td>Detection precision, recall and mAP across SNR conditions</td></tr>
</table>

The two settings provide complementary perspectives on AI-based radar processing. However, their outputs and evaluation metrics are task-dependent, and their experimental results are not directly interchangeable.
