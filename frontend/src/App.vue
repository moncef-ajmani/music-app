<template>
    <Header />
    <Hero />
    <div class="container">
        <div class="row">
            <div class="col-5">
                <Library :playlists="playlists.data"/>
            </div>
            <div class="col-7">
                <List :listData="uploads.music" :title="title"/>
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

    const title = "My Uploads";
    
    onMounted(async () => {
        try {
            const response = await fetch('http://localhost:5000/user/1/music');
            
            if (!response.ok) {
                throw new Error('Failed to fetch uploads');
            }
            uploads.value = await response.json();
            console.log(uploads.value);
        } catch (error) {
            console.error('Error fetching uploads:', error);
        }

        try {
            const response = await fetch('http://localhost:5000/user/1/playlists');
            
            if (!response.ok) {
                throw new Error('Failed to fetch playlists');
            }
            playlists.value = await response.json();
            console.log(playlists.value);
        } catch (error) {
            console.error('Error fetching playlists:', error);
        }
    });
</script>