# ExternalMemory.app
## my million dollar app idea

while shopping groceries i can never remember if i liked any of the beverages. i buy wine by bottle design. but this is annoying. so i had the idea of this app to assist me with previous impressions several years ago. you scan the barcode, provide any useful information and above all rate the product. once you rescan the barcode the previous rating will be remembered and displayed.

there are barcode and qr-code scanners, there might be product specific product comparing apps, but this is usable for every rateable product.

i had high hopes of publishing the app at the playstore and earning a little bit of it, maybe monetizing honest product ratings to the industry, but figured out an android app with python is ridiculously huge (@~50 mb for a basically feature-poor app like this), will hardly be downloaded and since when can industry and honesty be used in one sentence?

so if this idea goes viral without me participating in the earnings anyway: fuck you.

## [download a working apk from google drive](https://drive.google.com/file/d/1svrL37KDWVGNOJ2tptWggJMTWBPef0o_/view?usp=share_link)
(because tracking changes in this binary is a stupid idea). 

## features
* easy to use, open usecases
* stricly local
* no privacy issues
* export and restore database to and from shared storage
* good for your wallet and the environment
* keeps you from repetitive disappointments (at least some in your life)

![three screens](/images/screenshots.png)

## known flaws
* this app is far from perfect. i am just glad it essentially works and can be used as intended. 
* [see issues](/issues)

## <s>five simple steps</s> to create an app
<details>
<summary>you don't really want to read this</summary>

i imagine for some of you this is easy-peasy but trying to create this android app was a hell of a ride.

i don't know java and am still not willing to learn it. instead i wanted to rely an things i know. **boy, have i been naive!**

i still don't consider it bad to create an app with python for an amateur. but there were so much new things to learn i almost might as well have started learning a new language.

### framework
it took me at least a handful attempts to get in touch with [kivy][0] and it took me a while to figure out i had to run it in a virtual environment having to reinstall all necessary modules. the first somewhat running python-version came without the kv-language but i quickly figured out that this would be way messier in the end.
i found the documentation hard to comprehend but after a while it started to make sense. well, at least it worked somehow. on my pc.

### setting up the compiler environment - wtf?
so how about compiling? i have a windows only machine for several reasons and am totally fine with that. but buildozer for kivy needs a linux environment.
with absolutely no experience with unix systems i installed wsl, because why should i do another failing attempt in installing a linux distro that either does not work for me as my daily driver or isn't used later on anyway? and for compiling a cli-only system should absolutely suffice.
sure, as a virtual system python unsurprisingly required the installation of all my regular used modules another time. but that was only my first error message.
then i [installed buildozer][1]. with updating my .bashrc i had my first encounter with nano.
after [installing adb][2] on both, the host win10-system and the wsl, i tried to run buildozer. of course it was not that easy.
at some point i figured out that a connected android device might be needed. so i [checked adb devices][3] on both platforms.
after some failed attempts on the wsl i realized both platforms had different versions although both were a fresh installation from the same day.
so i had to find out how to obtain, [reinstall or rather overwrite adb on linux][4].

quite a bad feeling to look up every command like ls, mkdir, rm, rmdir, random sudo commands because i don't know shit about linux system structure.

the first attempt took a lot of time to download several libraries. it ran about half an hour before exiting with a ["missing am_iconv macro" error][5].
the second attempt exited with an error because i had one dependent module name wrong within the .spec-file
the third attempt was a somewhat successful build. beside the app quitting right after launch. so back to the drawing board.

i got errors stating android doesn't like 64bit architecture from modules with buildozers default settings for android.arch with armeabi_v7a.
arm64_v8a did't do the trick either.
several attempts to refactor everything to avoid opencv, using kivys camera (and it's inbuild cv) failed miserably.

as it turned out i tried to import the pc version of opencv with opencv-python instead of just opencv.
which requires [android sdk tools revision 14+][6], [cmake][7] and [android-ndk][8] as stated [here][9].

i lost passion and paused the project for a few months to concentrate on other projects. the last build installed the app on the phone but it would close itself on the spot as stated before. i had a hard time coming back. in the meantime i had upgraded to win11 and there might have been one or another upgrade to libraries. also i forgot everything learned previously about linux.

initially i researched for known issues with buildozer and opencv. one of the results contained the same error output as the repeated build-attempt: opencv required sdk tools rev 14, which was already satisfied. a closer look at search results got me to [this list][10]. after following all of the steps except the installation of android-studio (for snap install was not supported on wsl) a deletion of the .buildozer-directory and reinitialisation of the project was necessary for the update of the python-for-android-package with in the meantime required aap had not reached this place. running wsl in administrator mode finally resolved permission errors while downloading required packages and modules.

noteworthy might be that buildozer satisfied python 3.8.9 (most probably due to requirements) while the the installation of python3 declared no newer version than 3.6.8 would be available. whatever that means.

another long build later... (╯°□°）╯︵ ┻━┻

`adb logcat -d` showed *ImportError: ... cv2 is for EM_X86_64 (62) instead of EM_AARCH64 (183)* - had i repated the wrong requirement for opencv? after a change from opencv-python i suddenly got errors regarding unexpected numpy argument types. 

an upgrade of numpy was not possible for whatever reason, so i manually declared the latest version within the p4a-numpy-recipe. which lead to a successful build but the same error as before.


![you can hear this image](/images/ninemonthslater.png)

after having managed to successfully compile [my first running kivy-android-apk][11] i touched this again. in the meantime all of the setup-progress might have been overhauled for [this youtube-video][12] did indeed explain every step to compile a basic app (that doesn't need any permissions) - so half of my experiences were outdated.

in fact i did reset my wsl, reinstalled and didn't mind setting up a python environment with modules and dependencies at all. i did coding and testing on windows, copied the files to the ubuntu-wsl-directory and at least the buildozer worked in general. 

newly inspired and in hope time had developed python-for-android and its siblings in my favour i rewrote everything from scratch using kivyMD and storing by sqlite to the point where the application stood before: ui, detection of codes, storing, recognizing and some basic settings. on pc it worked as expected.

with my experiences in android permissions the next build was promising. permissions requested. no immediate shutdowns. ui displayed. 

![at least some progress](/images/itssomething.jpg)

still the camera wouldn't start streaming. in the meantime others had developed [similar questions][13], so i figured out opencv to be still problematic on android. on the other hand i had success trying kivys camera another time. hooray.

once the core features were working i omitted cloud synchronization in favour of exporting and importing the database file to the shared storage. more privacy, backup option and no hassle developing a clever synchronization algorithm while having a covid19-induced fever. still challenging enough. spend a good amount of time meddling around with plyer-filechooser and kivymd-filechooser which both had unexpected failures until i realized androidstorage4kivy has a chooser as well, and i need the module in either case. 


### most used terminal commands
* `buildozer android clean` after changes to the buildozer.spec-file
* `buildozer -v android debug` executes for recompiling even without connected device
* `adb logcat -s "python"` lists python related log entries only 

</details>


[0]: https://kivy.org/doc/stable/gettingstarted/installation.html
[1]: https://github.com/kivy/buildozer
[2]: https://www.xda-developers.com/install-adb-windows-macos-linux/
[3]: https://github.com/RobertFlatt/Android-for-Python/tree/main/Android-for-Python-Users#requirements
[4]: https://stackoverflow.com/questions/55634367/install-specific-adb-version-on-linux
[5]: https://github.com/FreeTDS/freetds/issues/172
[6]: https://gist.github.com/steveclarke/d988d89e8cdf51a8a5766d69ecb07e7b
[7]: https://graspingtech.com/upgrade-cmake/
[8]: https://stackoverflow.com/questions/26967722/how-to-install-android-ndk-in-linux
[9]: https://forum.opencv.org/t/run-samples-of-open-cv-in-android-studio/453/7
[10]: https://stackoverflow.com/questions/62582772/android-sdk-tools-opencv-requires-android-sdk-tools-revision-14-or-newer
[11]: https://github.com/erroronline1/customersurvey.py
[12]: https://www.youtube.com/watch?v=VsTaM057rdc
[13]: https://stackoverflow.com/questions/61122285/kivy-camera-application-with-opencv-in-android-shows-black-screen#answer-67061962