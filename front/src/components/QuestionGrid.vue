<template>
    <div class="question-grid">
        <div class="grid-block-q question-level">
            <b><center>Тема вопроса</center></b>
            <div>
                <slot name="q-level"></slot>
            </div>
        </div>
        <div class="grid-block-q question-type">
            <b><center>Тип вопроса</center></b>
            <div>
                <slot name="q-type"></slot>
            </div>
        </div>
        <div class="grid-block-q question-text">
            <b><center>Формулировка вопроса</center></b>
            <div>
                <slot name="q-text"></slot>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'QuestionGrid'
    }
</script>

<style>
  .question-grid{
    margin: 0 auto;
    width: 90vw;
    display: grid;
    grid-template-areas:
    "A A A A   A A B B   B B B B"
    "C C C C   C C C C   C C C C"
    "C C C C   C C C C   C C C C";
    row-gap: 25px;
    column-gap: 25px;
  }
  .question-level{
    grid-area: A;
  }
  .question-type{
    grid-area: B;
  }
  .question-text{
    grid-area: C;
  }
  .grid-block-q{
     border-radius: 15px;
     border: 2px solid #00415d;
     color: #00415d;
  }
</style>