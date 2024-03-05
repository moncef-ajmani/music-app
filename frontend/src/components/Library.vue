<template>
    <div class="library">
        <div class="library__header">
            <div class="library__header-title">Library</div>
            <!-- <div class="library__header-add"><img src="assets/images/plus.png"/></div> -->
        </div>
        <div class="library__list">
            <div class="library__list-item active" @click="callFetchUploads">
                <div class="library__list-item-image"><img src="@/assets/images/upload.png"/></div>
                <div class="library__list-item-content">
                    <div class="library__list-item-title">Uploads</div>
                    <div class="library__list-item-subtitle">Total • 3 songs</div>
                </div>
                <div class="library__list-item-addPlaylist">
                    <UploadMusic />
                </div>
            </div>
            <div class="library__list-item" @click="callFetchFavorits">
                <div class="library__list-item-image"><img src="@/assets/images/heart.png"/></div>
                <div class="library__list-item-content">
                    <div class="library__list-item-title">Likes</div>
                    <div class="library__list-item-subtitle">Total • 3 songs</div>
                </div>
            </div>
            <div class="library__list-item">
                <div class="library__list-item-image"><img src="@/assets/images/playlist.png"/></div>
                <div class="library__list-item-content">
                    <div class="library__list-item-title">Playlists</div>
                    <div class="library__list-item-subtitle">Total • 3 playlists</div>
                </div>
                <div class="library__list-item-addPlaylist">
                    <AddPlaylist />
                </div>
            </div>
            <div class="sub__list ml-5">
                <div class="library__list-item" v-for="(playlist,index) in playlists" :key="index">
                    <div class="library__list-item-image"><img :src="getBase64Image(playlist.image)" class="playlist-img"/></div>
                    <div class="library__list-item-content">
                        <div class="library__list-item-title">{{ playlist.name }}</div>
                        <div class="library__list-item-subtitle">Total • * songs</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import UploadMusic from './UploadMusic.vue';
    import AddPlaylist from './AddPlaylist.vue';

    const emit = defineEmits(['fetchFavorits','fetchUploads']);

    const callFetchFavorits = () =>{
        emit("fetchFavorits");
    }
    const callFetchUploads = () =>{
        emit("fetchUploads");
    }

    function getBase64Image(base64String) {
        return `data:image/jpeg;base64,${base64String}`;
    };

    const props = defineProps({
        playlists:{
            type: Array,
            required: true
        }
    })
</script>