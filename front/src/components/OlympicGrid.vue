<template>
    <div class="olympic-grid">
        <center><b><slot name="q-header"></slot></b></center>
        <div class="grid-block question-theme">
            <center><b>Тема</b></center>
            <div>
                <slot name="q-theme"></slot>
            </div>
        </div>
        <div class="grid-block question-wording">
            <div>
                <slot name="q-word"></slot>
            </div>
        </div>
        <div class="grid-block question-answer">
            <div>
                <slot name="q-answer"></slot>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'OlympicGrid'
    }
</script>

<style>
  .olympic-grid{
    margin: 0 auto;
    padding: 10px 10px 10px 10px;
    width: 90vw;
    display: grid;
    grid-template-areas:
    "A A A A   A A A A   A A A A"
    "B B B B   B B B B   B B B B"
    "C C C C   C C C C   C C C C";
    row-gap: 25px;
    border: 2px solid #00415d;
    border-radius: 15px;
  }
  .question-theme{
    grid-area: A;
  }
  .question-wording{
    grid-area: B;
  }
  .question-answer{
    grid-area: C;
  }
  .grid-block{
    border: none;
    color: #00415d;
  }
</style>