<template>
    <div class="player">
        <!-- <div class="player__music">
            <div class="player__music-image">
                <img :src="getBase64Image(current?.image)"/>
                
            </div>
            <div class="player__music-content">
                <div class="player__music-title">{{ this.current?.title }}</div>
                <div class="player__music-artist">{{ current?.artist }}</div>
            </div>
            <div class="player__music-like"><img src="@/assets/images/plus.png"/></div>
        </div> -->
       
        <div class="player__contols">
            <div class="player__contols-btns">
                <div class="player__btn-suffle" @click="shuffle">
                    <img src="@/assets/images/shuffle.png"/>
                </div>
                <div class="player__btn-prev" @click="playPrevious">
                    <img src="@/assets/images/previous.png"/>
                </div>
                <div class="player__btn-play" @click="play">
                    <img src="@/assets/images/play-button.png"/>
                </div>
                <div class="player__btn-next" @click="playNext">
                    <img src="@/assets/images/next.png" />
                </div>
                <div class="player__btn-repeat" @click="repeat">
                    <img src="@/assets/images/repeat.png"/>
                </div>
            </div>
            <div class="player__contols-progress">
                <!-- <div class="player__contols-progress-time">1:22</div> -->
                <div class="player__contols-progress-bar">
                    <!-- <progress value="3" max="10"></progress> -->
                    
                    <audio ref="audioPlayer" controls></audio>
                </div>
                <!-- <div class="player__contols-progress-time-total">2:15</div> -->
            </div>
        </div>
        <!-- <div class="player__volume">
            <img src="@/assets/images/volume.png" alt="">
            <progress value="3" max="10"></progress>
            <div>{{ queue?.length }}</div>
        </div> -->
        
        <!-- <audio controls :src="getBase64Audio(props?.musics[0].mp3_file)"></audio> -->
    </div>
</template>

<script>
import { defineProps } from 'vue';

export default {
  props: {
    queue: {
      type: Array
    },
    current: {
      type: Object
    }
  },
  data() {
    return {
        isPlaying: false,
        currentIndex: 0,
        isRepeatOne: false,
    };
  },
  methods: {
    play() {
        if (!this.$refs.audioPlayer.paused) {
            console.log("pause",this.currentIndex);
            this.$refs.audioPlayer.pause();
            this.isPlaying = false;
        } else {
            if (this.queue.length > 0) {
                if (!this.$refs.audioPlayer.src) {

                    this.$refs.audioPlayer.src = this.getBase64Audio(this.queue[this.currentIndex].mp3_file);
                }
                console.log("play",this.currentIndex);
                this.$refs.audioPlayer.play();
                this.isPlaying = true;
            }
        }
    },
    playPrevious() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.$refs.audioPlayer.src = this.getBase64Audio(this.queue[this.currentIndex].mp3_file);
            this.play();
        } else {
            this.currentIndex = this.queue.length - 1;
            this.$refs.audioPlayer.src = this.getBase64Audio(this.queue[this.currentIndex].mp3_file);
            this.play();
        }
        console.log("play previous",this.currentIndex);
    },
    playNext() {
        if (this.currentIndex < this.queue.length - 1) {
            this.currentIndex++;
            this.$refs.audioPlayer.src = this.getBase64Audio(this.queue[this.currentIndex].mp3_file);
            this.play();
        } else {
            this.currentIndex = 0;
            this.$refs.audioPlayer.src = this.getBase64Audio(this.queue[this.currentIndex].mp3_file);
            this.play();
        }
        console.log("play next",this.currentIndex);
    },
    shuffle() {
        console.log("shuffle");
        this.queue = this.queue.sort(() => Math.random() - 0.5);
    },
    repeat() {
        console.log("repeat");
        this.isRepeatOne = !this.isRepeatOne;
    },
    getBase64Image(base64String) {
        return `data:image/jpeg;base64,${base64String}`;
    },
    getBase64Audio(base64String) {
        return `data:audio/mp3;base64,${base64String}`;
    },
  },
  mounted() {
    // Listen for the 'ended' event of the audio element
    this.$refs.audioPlayer.addEventListener('ended', () => {
        this.playNext(); // When the current music ends, play the next one
    });
  }
};
</script>

