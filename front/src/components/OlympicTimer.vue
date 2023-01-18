<template>
<nav class="nav__timer">
    <div class="div-timer">
        <slot name="timer"></slot>
    </div>
</nav>
</template>

<script>
 export default {
    name: "OlympicTimer",
    props: {
        timeLeft: {
          type: Number,
          required: true
        }
    }
 }
</script>

<style>
    .nav__timer {
         position: fixed;
         right: 0;
         top: 0;
         width: 150px;
         z-index: 100;
         background-color: #00415d;
         overflow: hidden;
         box-shadow: 4px 7px 10px rgba(0, 0, 0, .4);
         border-radius: 25px;
    }
    .div-timer {
        color: white;
        font-size: 28px;
        text-align: center;
    }
    .base-timer__label {
         position: absolute;
        /* Size should match the parent container */
         width: 300px;
         height: 300px;
        /* Keep the label aligned to the top */
         top: 0;
        /* Create a flexible box that centers content vertically and horizontally */
         display: flex;
         align-items: center;
         justify-content: center;
        /* Sort of an arbitrary number;
         adjust to your liking */
         font-size: 48px;
    }
</style>