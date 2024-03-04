<template>
    <Header />
    <Hero />
    <div class="container">
        <div class="row">
            <div class="col-5">
                <Library />
            </div>
            <div class="col-7">
                <List :listData="data.music" :title="title"/>
            </div>
        </div>
    </div>
    
    <Player :music="data"/>
</template>
<script setup>
    import Header from './components/Header.vue';
    import Hero from './components/Hero.vue';
    import Library from './components/Library.vue';
    import List from './components/List.vue';
    import Player from './components/Player.vue';
    import { ref, onMounted } from 'vue';
    import axios from 'axios';

    const bytes = []

    const data = ref([]);
    const title = "My Uploads";
    onMounted(async () => {
        try {
            const response = await fetch('http://localhost:5000/user/1/music');
            
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            data.value = await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });
</script>