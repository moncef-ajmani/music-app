<template>
    <div class="list">
      <div class="list__header">
        <div class="list__header-title">{{ title }}</div>
        <div class="list__header-controls">
          <div class="control play"><img src="@/assets/images/play.png" /></div>
          <div class="control shuffle"><img src="@/assets/images/shuffle.png" /></div>
          <div class="control download"><img src="@/assets/images/download.png" /></div>
        </div>
      </div>
      <div class="list__items">
        <div class="list__item" v-for="(item, index) in listData" :key="index">
          <div class="list__item-id">{{ index + 1 }}</div>
          <div class="list__item-image">
            <img :src="getBase64Image(item.image)" alt="">
          </div>
          <div class="list__item-like"><img src="@/assets/images/heart.png" :if="item.like"/></div>
          <div class="list__item-title">{{ item.title }}</div>
          <div class="list__item-artist">{{ item.artist }}</div>
          <div class="list__item-time">2:20</div>
          <!-- <audio controls :src="getBase64Audio(item.mp3_file)" v-if="item.mp3_file"></audio> -->
        </div>
      </div>
    </div>
    
</template>
  
<script setup>
    import { defineProps } from 'vue';

    function getBase64Image(base64String) {
        return `data:image/jpeg;base64,${base64String}`;
    };

    function getBase64Audio(base64String) {
        return `data:audio/mp3;base64,${base64String}`;
    }
    const props = defineProps({
        listData: {
          type: Array,
          required: true
        },
        title: {
          type: String,
          required: true
        },
       
    });
    
</script>
  