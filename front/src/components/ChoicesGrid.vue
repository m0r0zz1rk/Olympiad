<template>
    <div class="choices-grid">
        <div class="grid-block-ch first-choice">
            <slot name="first-choice"></slot>
        </div>
        <div class="grid-block-ch second-choice">
            <slot name="second-choice"></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ChoicesGrid'
    }
</script>

<style>
  .choices-grid{
    margin: 0 auto;
    width: 90%;
    display: grid;
    grid-template-areas:
    "A A A A   A A B B   B B B B"
    "A A A A   A A B B   B B B B"
    "A A A A   A A B B   B B B B";
    column-gap: 20px;
    padding-bottom: 10px;
    padding-top: 10px;
  }
  .first-choice{
    grid-area: A;
  }
  .second-choice{
    grid-area: B;
  }
  .grid-block-ch{
     width: 25vw;
     height: 75px;
     margin: 0 auto;
     align-items: center;
     vertical-align: middle;
     justify-content: center;
     border-radius: 15px;
     border: 2px solid #00415d;
     color: #00415d;
  }
</style>