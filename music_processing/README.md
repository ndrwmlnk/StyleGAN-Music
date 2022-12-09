# Music processing

The jupyter notebook is meant as an interactive script for experimenting with different features and parameters. It runs well on

* Python 3.8
* librosa 0.9.2
* matplotlib 3.5.0
* numpy 1.20.3
* moviepy 1.0.3

To generate a video with music, you can run the `generate_video()` function which in its current state creates the three dimensions __bass frequency__, __spectral centroid__ and __vocal activation__ and couples them to the (also 3d) image set.

* bass frequency: The audio signal is separated into transient and harmonic parts. The transient part is then run through an fft to seperate it into frequency bins. A low frequency bin is then isolated and smoothed / filtered so that it resembles clear peaks that correspond to base drum hits in the music.
* spectral centroid: The whole audio signal is run through a filter than calculates the spectral centroid for each time step. This roughly corresponds to the average frequency of the track at that given time.
* vocal activation: The isolated vocals are processed and normalized and are then used to control a sinusoid curve. If the vocal audio is above a certain threshold, then the sinusoid is activated, else the signal is 0.


You need to provide at least the following information:

* `audio_path`: Points to the music file
* `vocal_path`: Points to the file with isolated vocals (vocal separation is not done on the fly for performance reasons. If you want to try out different songs, you need to separate the vocals with something like demucs)
* `video_path`: specify the folder where the images for the video are saved at
* `image_filetype`: filetype of the image files (at least png and jpg should be accepted). Default to ".png"
* `image_filename`: the schema of the image names where "dim1" to "dim3" are replaced with the according dimensions. Default to "dim1-dim2-dim3"
* `output_path`: Points to the video file that you want to generate. Different video file types are supported. Default to "video.mp4"

The function can be finetuned according to the following parameters:

* `image_steps`: This is the resolution of each dimension, i.e. the number of images per channel. Default to 20
* `image_index_start`: The first index of the image files (relevant if you start at 0 or at 1). Default to 1
* `transients_Only`: if this option is set to True, then the bass frequency band will only listen to the transients of the spectrum and not the harmonic elements. Leads to a more tight percussive effect. Default to True
* `frame_rate`: The frame rate of the video. Default to 30
* `frame_smoothing`: A 1d gaussian convolution is applied to the audio curves to remove stuttering. This parameter sets the window size in frames. Default to 4.
* `spike_factor`: An exponential filter is applied to the curves in order to pull down the lows and spike the highs. This parameter sets the strength of this filter. Default to 4
* `bass_freq`: Sets the frequency that will pick up the bass band (in Hz). Default to 55
* `sinusoid_freq`: Sets the frequency of the sinusoid undulation (in Hz). Default to 1
* `sinusoid_threshold`: Sets the threshold (as a fraction of the maximum energy) above which the sinusoid should be activated. Default to .1
* `local_max_threshold`: Sets the threshold (as a fraction of the global maximum energy) above which a measure of the bass frequency should be locally maximized to 0 and 1. Default to .6


If you want to change one of the dimensions completely (for example, instead of bass you want some kind of switching on and off of a signal), you will need to hard-code it into the function or use your own function. The important part is that whatever you feed into `audio_curve_to_video_3d()` at the end, is a 1d array with the frame-rate of the final video where each frame is a discrete step that range over the resolution of the image dimensions.


All functions are commented so that the processes and calculations should be self-explanatory. Most of the processing is done in numpy and librosa and you can look at their docs for the documentation of their built-in functions.

Some example image and music files can be found [here](https://uni-bielefeld.sciebo.de/s/HLvwgO7BUbMuepL).
