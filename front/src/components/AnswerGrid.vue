<template>
    <div class="answer-grid">
        <div class="grid-block-answ answer-main">
            <div>
                <slot name="a-main"></slot>
            </div>
        </div>
        <div class="grid-block-answ answer-additional">
            <div>
                <slot name="a-additional"></slot>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'AnswerGrid'
    }
</script>

<style>
  .answer-grid{
    margin: 0 auto;
    width: 90vw;
    display: grid;
    grid-template-areas:
    "A A A A   A A A A   A A A A"
    "A A A A   A A A A   A A A A"
    "B B B B   B B B B   B B B B";
    row-gap: 25px;
    column-gap: 25px;
  }
  .answer-main{
    grid-area: A;
  }
  .answer-additional{
    grid-area: B;
  }
  .grid-block-answ{
     border-radius: 15px;
     border: 2px solid #00415d;
     color: #00415d;
  }
</style>