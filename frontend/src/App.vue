<template>
    <Header />
    <Hero />
    
    <div class="container">
        <div class="row" v-if="isLoggedIn">
            <div class="col-5">
                <Library :playlists="playlists.data" @fetchUploads="fetchUploads" @fetchFavorits="fetchFavorits" @fetchPlaylistById="fetchPlaylistById" /> 
            </div>
            <div class="col-7">
                <List :playlists="playlists.data" :listData="data.music" :title="title" @fetchUploads="fetchUploads" @fetchFavorits="fetchFavorits" @setCurrentMusic="setCurrentMusic"/>
            </div>
        </div>
        <h2 class="m-5" v-else >You Should Login!!</h2>
    </div>

    <Player :queue="data.music" :current="currentMusic" />
</template>
<script setup>
    import Header from './components/Header.vue';
    import Hero from './components/Hero.vue';
    import Library from './components/Library.vue';
    import List from './components/List.vue';
    import Player from './components/Player.vue';
    import { ref, onMounted } from 'vue';

    const isLoggedIn = typeof localStorage !== 'undefined' && localStorage.getItem("user_id");

    const uploads = ref([]);
    const playlists = ref([]);
    const data = ref([]);
    const currentMusic = ref(null);

    const title = ref("My Uploads");
    
    onMounted(async () => {
        await fetchUploads();
        await fetchPlaylists();
    });

    async function fetchFavorits(){
        try {
            const response = await fetch(`http://localhost:5000/user/${localStorage.getItem("user_id")}/favorits`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch playlists');
            }
            data.value = await response.json();
            title.value = "My Likes";
            console.log("Favorits: ",data.value);
        } catch (error) {
            console.error('Error fetching playlists:', error);
        }
    }
    function setCurrentMusic(music){
        console.log("current:",music);
        // console.log(data.value);
        currentMusic.value = music;
    }
    async function fetchPlaylists(){
        try {
            const response = await fetch(`http://localhost:5000/user/${localStorage.getItem("user_id")}/playlists`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch playlists');
            }
            playlists.value = await response.json();
            console.log("Playlists: ",playlists.value);
        } catch (error) {
            console.error('Error fetching playlists:', error);
        }
    }
    async function fetchUploads(){
        try {
            const response = await fetch(`http://localhost:5000/user/${localStorage.getItem("user_id")}/music`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch uploads');
            }
            data.value = await response.json();
            title.value = "My Uploads";
            console.log("Uploads: ",data.value);
        } catch (error) {
            console.error('Error fetching uploads:', error);
        }
    }
    async function fetchPlaylistById(playlist_id,name){
        console.log("fetch playlist by id: ",playlist_id);
        try {
            const response = await fetch(`http://localhost:5000/playlist/${playlist_id}/music`)
            
            if (!response.ok) {
                throw new Error('Failed to fetch playlist');
            }
            data.value = await response.json();
            title.value = name;
            console.log(`Playlist ${playlist_id}: ${data.value}`);
        } catch (error) {
            console.error('Error fetching playlist:', error);
        }
    }
</script>