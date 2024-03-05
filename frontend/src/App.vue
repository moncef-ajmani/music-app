<template>
    <Header />
    <Hero />
    <div class="container">
        <div class="row">
            <div class="col-5">
                <Library :playlists="playlists.data" @fetchUploads="fetchUploads" @fetchFavorits="fetchFavorits" /> 
            </div>
            <div class="col-7">
                <List :playlists="playlists.data" :listData="data.music" :title="title" @fetchUploads="fetchUploads" @fetchFavorits="fetchFavorits"/>
            </div>
        </div>
    </div>
    
    <Player :music="uploads"/>
</template>
<script setup>
    import Header from './components/Header.vue';
    import Hero from './components/Hero.vue';
    import Library from './components/Library.vue';
    import List from './components/List.vue';
    import Player from './components/Player.vue';
    import { ref, onMounted } from 'vue';

    const uploads = ref([]);
    const playlists = ref([]);
    const data = ref([]);

    const title = "My Uploads";
    
    onMounted(async () => {
        await fetchUploads();
        await fetchPlaylists();
    });

    async function fetchFavorits(){
        try {
            const response = await fetch('http://localhost:5000/user/1/favorits');
            
            if (!response.ok) {
                throw new Error('Failed to fetch playlists');
            }
            data.value = await response.json();
            console.log("Favorits: ",data.value);
        } catch (error) {
            console.error('Error fetching playlists:', error);
        }
    }

    async function fetchPlaylists(){
        try {
            const response = await fetch('http://localhost:5000/user/1/playlists');
            
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
            const response = await fetch('http://localhost:5000/user/1/music');
            
            if (!response.ok) {
                throw new Error('Failed to fetch uploads');
            }
            data.value = await response.json();
            console.log("Uploads: ",data.value);
        } catch (error) {
            console.error('Error fetching uploads:', error);
        }
    }
</script>