<template>
  <router-view/>
</template>

<style>
#app {
    width: 100vw;
    height: 100vh;
    display: block;
    vertical-align: middle;
}
#main-content, #load{
    display: flex;
    width: 100%;
    margin: auto;
    justify-content: center;
    text-align: center;
}
.vue-active{
    display: block;
    visibility: visible;
    pointer-events: auto;
}
.vue-deactive{
    display: none;
    visibility: collapse;
    pointer-events: none;
}
</style>

<script>
    export default {

    }
</script>
