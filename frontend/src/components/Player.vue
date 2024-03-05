<template>
    <div class="player">
        <div class="player__music">
            <div class="player__music-image">
                <img src="@/assets/images/music.png" />
            </div>
            <div class="player__music-content">
                <div class="player__music-title">212</div>
                <div class="player__music-artist">Dada, Rita Kamale, NAB FAKE</div>
            </div>
            <div class="player__music-like"><img src="@/assets/images/plus.png"/></div>
        </div>
        <div class="player__contols">
            <div class="player__contols-btns">
                <div class="player__btn-suffle">
                    <img src="@/assets/images/shuffle.png"/>
                </div>
                <div class="player__btn-prev">
                    <img src="@/assets/images/previous.png"/>
                </div>
                <div class="player__btn-play">
                    <img src="@/assets/images/play-button.png"/>
                </div>
                <div class="player__btn-next">
                    <img src="@/assets/images/next.png"/>
                </div>
                <div class="player__btn-repeat">
                    <img src="@/assets/images/repeat.png"/>
                </div>
            </div>
            <div class="player__contols-progress">
                <div class="player__contols-progress-time">1:22</div>
                <div class="player__contols-progress-bar"><progress value="3" max="10"></progress></div>
                <div class="player__contols-progress-time-total">2:15</div>
            </div>
        </div>
        <div class="player__volume">
            <img src="@/assets/images/volume.png" alt="">
            <progress value="3" max="10"></progress>
        </div>
    </div>
</template>

<script setup>
    import { defineProps, onMounted, ref } from 'vue';
    const props = defineProps({
        music: {
            type: Array,
            required: true
        }
    });

    let isPlaying = false;
    let currentTime = 0;
    let totalTime = 0;
    let volume = 0.5;
    let audio = new Audio();
    const musicTitle = ref("");
    const musicArtist = ref("");
    const audioBytes = ref("");

      
    onMounted(()=> {
        // console.log(props);
        // musicTitle = props.music[0].title;

        // Set audio source
        audio.src = "data:audio/mpeg;base64," + audioBytes;

        // Listen for audio events
        audio.addEventListener('loadedmetadata', () => {
            totalTime = audio.duration;
        });

        audio.addEventListener('timeupdate', () => {
            currentTime = audio.currentTime;
        });

        audio.addEventListener('ended', () => {
            isPlaying = false;
        });
    }),
   
    function togglePlay() {
        if (isPlaying) {
            audio.pause();
        } else {
            audio.volume = volume;
            audio.play();
        }
        isPlaying = !isPlaying;
    }
    function formatTime(seconds) {
        const min = Math.floor(seconds / 60);
        const sec = Math.floor(seconds % 60);
        return `${min}:${sec < 10 ? '0' : ''}${sec}`;
    }
    function seek(event) {
        audio.currentTime = event.target.value;
    }
</script>