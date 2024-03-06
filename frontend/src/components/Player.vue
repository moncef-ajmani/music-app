<template>
    <div class="player" v-if="current">
        <div class="player__music">
            <div class="player__music-image">
                <img :src="getBase64Image(current?.image)"/>
            </div>
            <div class="player__music-content">
                <div class="player__music-title">{{ current?.title }}</div>
                <div class="player__music-artist">{{ current?.artist }}</div>
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
                <div class="player__contols-progress-bar">
                    <!-- <progress value="3" max="10"></progress> -->
                    <audio controls :src="getBase64Audio(queue)"></audio>
                </div>
                <div class="player__contols-progress-time-total">2:15</div>
            </div>
        </div>
        <div class="player__volume">
            <img src="@/assets/images/volume.png" alt="">
            <progress value="3" max="10"></progress>
            <div>{{ queue?.length }}</div>
            
        </div>
        
    </div>
</template>

<script setup>
    import { defineProps } from 'vue';
    const props = defineProps({
        queue:{
            type:Array
        },
        current:{
            type:Object
        }
    });
    function getBase64Image(base64String) {
        return `data:image/jpeg;base64,${base64String}`;
    };

    function getBase64Audio(base64String) {
        return `data:audio/mp3;base64,${base64String}`;
    }

    let songsIndex = 1;
    // Initially load song info
    loadSong(songs[songsIndex])

    function loadSong(){

    }

</script>