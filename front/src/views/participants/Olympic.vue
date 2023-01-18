<template>
    <ParticipantHeader />
    <OlympicTimer
      :time-left="timeLeft">
        <template v-slot:timer>
            {{ formattedTimeLeft }}
        </template>
    </OlympicTimer>
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../assets/gifs/load.gif">
            <br><b style="color: #00415d;">{{ info }}</b>
        </div>
        <div v-bind:class="[ContentClass]">
            <div v-for="question in listQuestions">
                <OlympicGrid>
                    <template v-slot:q-theme>
                        <b><h3>{{ question[1] }}</h3></b>
                    </template>
                    <template v-slot:q-word>
                        <hr style="border: 1px solid; background-color: #00415d;">
                        <div v-html="question[2]"></div><br>
                        <hr style="border: 1px solid #00415d;">
                    </template>
                    <template v-slot:q-answer>
                        <div v-if="question[3] === 'Классический'">
                            <div class="container-table" style="width: 80%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th colspan="2">Выберите правильный вариант ответа</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        <ChoicesGrid v-for="sl in chunkedArr(question[0])">
                                            <template v-slot:first-choice>
                                                    <div
                                                    :class="['choice-parent', { 'picked-choice' : sl[0] == pickedChoices[question[0]] }]">
                                                        <div class="choice-child"
                                                        @click="event => giveChoice(event, question[0], sl[0])">
                                                            {{ sl[0] }}
                                                        </div>
                                                    </div>
                                            </template>
                                            <template v-slot:second-choice>
                                                    <div
                                                    :class="['choice-parent', { 'picked-choice' : sl[1] == pickedChoices[question[0]] }]"
                                                    >
                                                        <div class="choice-child"
                                                        @click="event => giveChoice(event, question[0], sl[1])">
                                                            {{ sl[1] }}
                                                        </div>
                                                    </div>
                                            </template>
                                        </ChoicesGrid>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div v-if="question[3] === 'Соответствие'">
                            <div class="container-table" style="width: 65%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th colspan="2">Выберите нужное значение из выпадающего списка на каждой строке</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="label in getLabels(question[0])">
                                                <td>{{ label }}</td>
                                                <td>
                                                    <select class="form-control text-center"
                                                        @change="event => giveAccAnswer(event, question[0], label)">
                                                        <option v-for="poss in getPossibles(question[0])"
                                                            :selected="listAccAnswers[question[0]+`-`+label] == poss">
                                                            {{ poss }}
                                                        </option>
                                                    </select>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div v-if="question[3] === 'Развернутый ответ'">
                            <div class="container-table" style="width: 65%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th>Заполните поле для ответа ниже</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <textarea :id="`detailed_`+question[0]" class="form-control"
                                                        v-model="questionsDetailedAnswers[question[0]]"
                                                        @change="event => giveDetailedAnswer(event, question[0])"></textarea>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div v-if="question[3] === 'Краткий ответ'">
                            <div class="container-table" style="width: 65%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th colspan="2">Впишите ответ в поле ниже</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>{{ takeShortLabel(question[0])[1] }}</td>
                                                <td>
                                                    <input type="text" class="form-control text-center"
                                                        v-model="questionsShortAnswers[question[0]]"
                                                        @change="event => giveShortAnswer(event, takeShortLabel(question[0])[0], question[0])">
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div v-if="question[3] === 'Табличный'">
                            <div class="container-table">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th :colspan="questionColumns(question[0]).length+1">Заполните таблицу</th>
                                            </tr>
                                            <tr>
                                                <th>Подпись к ответу\Столбцы</th>
                                                <th v-for="col in questionColumns(question[0])">
                                                    {{ col[1] }}
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="row in questionRows(question[0])">
                                                <td>{{ row[1] }}</td>
                                                <td v-for="col in questionColumns(question[0])">
                                                    <input type="text" class="form-control text-center"
                                                        v-model="questionsTableAnswers[question[0]+`-`+col[0]+`-`+row[0]]"
                                                        @change="event => giveTableAnswer(event, question[0], col[0], row[0])">
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </template>
                </OlympicGrid><br>
            </div>
            <button class="btn btn-lg btn-primary m-auto iohk-butt"
                type="button" @click="endOlymp('button');">
                Завершить
            </button>
        </div>
    </div>
</template>

<script>
    import ParticipantHeader from "../../components/ParticipantHeader.vue"
    import OlympicGrid from "../../components/OlympicGrid.vue"
    import ChoicesGrid from "../../components/ChoicesGrid.vue"
    import OlympicTimer from "../../components/OlympicTimer.vue"

    export default {
        name: "Olympic",
        components: {
            ParticipantHeader,
            OlympicGrid,
            ChoicesGrid,
            OlympicTimer
        },
        data() {
            return {
                info: 'Формируем страницу с вопросами...',
                timerInterval: null,
                checkEnd: null,
                timeLimit: 480,
                timePassed: 0,
                pickedChoices: [],
                listQuestions: [],
                questionsPossibles: [],
                questionsAccLabels: [],
                listSimpleAnswers: [],
                listShortAnswers: [],
                listAccAnswers: [],
                listChoices: [],
                questionsCells: [],
                questionsTableColumns: [],
                questionsTableRows: [],
                questionsPossValues: [],
                questionsTableAnswers: [],
                questionsShortAnswers: [],
                questionsDetailedAnswers:[],
                answers: [],
                answersChoice: [],
                questionTheme: '',
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                sort: '-date_event'
            }
        },
        computed: {
            formattedTimeLeft() {
              const timeLeft = this.timeLeft
              // The largest round integer less than or equal
              //   to the result of time divided being by 60.
              const minutes = Math.floor(timeLeft / 60)
              // Seconds are the remainder of the time divided
              //   by 60 (modulus operator)
              let seconds = timeLeft % 60
              // If the value of seconds is less than 10,
              //   then display seconds with a leading zero
              if (seconds < 10) {
                seconds = `0${seconds}`
              }
              // The output in MM:SS format
              return `${minutes}:${seconds}`
            },
            timeLeft() {
              return this.timeLimit - this.timePassed
            }
        },
        methods: {
            async getRemainingTime() {
                let that = this
                let response = await fetch(this.$store.state.backendUrl+'/api/participants/get_time/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => {
                    if (resp.status == 200) {
                          return resp.json()
                      } else {
                         showBanner('.banner.error', 'Произошла ошибка, повторите попытку')
                         that.$router.push('/start')
                         return false
                      }
                })
                this.timeLimit = response.success
                this.startTimer()
                this.checkEndOlymp()
            },
            startTimer() {
              let tl = parseInt(this.timeLimit)
              let tp = parseInt(this.timePassed)
              let that = this
              this.timerInterval = setInterval(() => {
                if (tl > tp) {
                    tp += 1
                    that.timePassed = tp
                }
              }, 1000);
            },
            checkEndOlymp() {
                this.checkEnd = setInterval(() => {
                    if (this.timeLimit <= this.timePassed) {
                        this.endOlymp('timer')
                    }
                }, 1000);
            },
            chunkedArr(question_id) {
                const result = []
                $.each(this.listChoices, function(index, chs) {
                    if (index == question_id) {
                        for (let i = 0; i < chs.length; i += 2) {
                            result.push(chs.slice(i, i + 2))
                        }
                    }
                })
                return result
            },
            questionColumns(question_id) {
                let list = []
                $.each(this.questionsTableColumns, function(index, q){
                    if (index == question_id) {
                        $.each(q, function(index_c, col){
                            list.push([index_c, col])
                        })
                    }
                })
                return list
            },
            questionRows(question_id) {
                let list = []
                $.each(this.questionsTableRows, function(index, q){
                    if (index == question_id) {
                        $.each(q, function(index_r, row){
                            list.push([index_r, row])
                        })
                    }
                })
                return list
            },
            async getQuestionCells() {
                this.questionsCells = await fetch(this.$store.state.backendUrl+'/api/participants/get_table/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
                let that = this
                $.each(this.questionsCells, function(index, row) {
                    $.each(row, function(i, value) {
                        that.questionsTableAnswers[index+'-'+i] = value
                    })
                })
            },
            async getSimpleAnswers() {
                this.listSimpleAnswers = await fetch(this.$store.state.backendUrl+'/api/participants/get_simple/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
                let that = this
                $.each(this.listSimpleAnswers, function(index, answer) {
                    that.questionsDetailedAnswers[index] = answer
                })
            },
            async getShortAnswers() {
                this.listShortAnswers = await fetch(this.$store.state.backendUrl+'/api/participants/get_short/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
                let that = this
                $.each(this.listShortAnswers, function(index, row) {
                    that.questionsShortAnswers[index] = row[2]
                })
            },
            async getAccAnswers() {
                this.listAccAnswers = await fetch(this.$store.state.backendUrl+'/api/participants/take_acc_answers/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
            },
            async getQuestionsPossibles() {
                this.questionsPossibles = await fetch(this.$store.state.backendUrl+'/api/participants/take_possible/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
            },
            async getChoices() {
                this.listChoices = await fetch(this.$store.state.backendUrl+'/api/participants/take_choices/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
            },
            async getParticipantChoices() {
                this.pickedChoices = await fetch(this.$store.state.backendUrl+'/api/participants/take_part_choices/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
            },
            getPossibles(question_id) {
                let l = []
                $.each(this.questionsPossibles, function(index, list) {
                    if (index == question_id) {
                        l = list
                        return false
                    }
                })
                return l
            },
            async getQuestionsAccLabels() {
                this.questionsAccLabels = await fetch(this.$store.state.backendUrl+'/api/participants/take_acc_labels/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                  })
                })
                .then(resp => resp.json())
            },
            getLabels(question_id) {
                let l = []
                $.each(this.questionsAccLabels, function(index, list) {
                    if (index == question_id) {
                        l = list
                        return false
                    }
                })
                return l
            },
            takeTableAnswer(question_id, col_id, seq_number) {
                let val = ''
                $.each(this.questionsCells, function(index, row) {
                    if (index == question_id) {
                        $.each(row, function(i, value) {
                            if (i == col_id+'-'+seq_number) {
                                val = value
                                return false
                            }
                        })
                    }
                })
                return val
            },
            async giveTableAnswer(event, question_id, col_id, seq_number) {
                await fetch(this.$store.state.backendUrl+'/api/participants/save_table/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'question_id': question_id,
                    'col_id':col_id,
                    'seq_number': seq_number,
                    'answer': event.target.value
                  })
                })
                .then(resp => resp.json())
            },
            async giveDetailedAnswer(event, question_id) {
                await fetch(this.$store.state.backendUrl+'/api/participants/save_detailed/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'question_id': question_id,
                    'answer': event.target.value
                  })
                })
                .then(resp => resp.json())
            },
            takeShortLabel(question_id) {
                let arr = []
                $.each(this.listShortAnswers, function(index, row) {
                    if (index == question_id) {
                        arr = row
                        return false
                    }
                })
                return arr
            },
            async giveShortAnswer(event, answer_id, question_id) {
                await fetch(this.$store.state.backendUrl+'/api/participants/save_short/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'question_id': question_id,
                    'answer_id': answer_id,
                    'answer': event.target.value
                  })
                })
                .then(resp => resp.json())
            },
            async giveAccAnswer(event, question_id, label) {
                await fetch(this.$store.state.backendUrl+'/api/participants/save_acc/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'question_id': question_id,
                    'label': label,
                    'answer': event.target.value
                  })
                })
                .then(resp => resp.json())
            },
            async giveChoice(event, question_id, choice) {
                await fetch(this.$store.state.backendUrl+'/api/participants/save_choice/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'question_id': question_id,
                    'answer': choice
                  })
                })
                .then(resp => resp.json())
                this.getParticipantChoices()
            },
            async getTableColumns() {
                let url = this.$store.state.backendUrl+'/api/participants/question_cols/'
                this.questionsTableColumns = await fetch(url, {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid')
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            async getTableRows() {
                let url = this.$store.state.backendUrl+'/api/participants/question_rows/'
                this.questionsTableRows = await fetch(url, {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid')
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            async getQuestions() {
               this.listQuestions = await fetch(this.$store.state.backendUrl+'/api/participants/participant_questions/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid')
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
                this.getRemainingTime()
                this.getTableColumns()
                this.getTableRows()
                this.getQuestionCells()
                this.getSimpleAnswers()
                this.getShortAnswers()
                this.getQuestionsPossibles()
                this.getQuestionsAccLabels()
                this.getAccAnswers()
                this.getChoices()
                this.getParticipantChoices()
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            async getQuestionTheme() {
                this.questionTheme = await fetch(this.$store.state.backendUrl+'/api/participants/participant_questions/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid')
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            endOlymp(type) {
                if (type == 'button') {
                    if (confirm('Вы уверены, что хотите завершить прохождение олимпиады?')){
                        this.endOlympProcess()
                    }
                } else {
                    this.endOlympProcess()
                }
            },
            async endOlympProcess() {
                clearInterval(this.checkEnd);
                this.info = 'Заврешаем прохождение олимпиады...'
                this.LoadClass = 'vue-active'
                this.ContentClass = 'vue-deactive'
                await fetch(this.$store.state.backendUrl+'/api/participants/olympiad_stop/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid')
                  })
                })
                .then(resp => {
                  showBanner('.banner.success', 'Олимпиада успешно завершена. Спасибо за участие!')
                      this.$router.push('/sign-in')
                })
            },
            leaving(event) {
                fetch(this.$store.state.backendUrl+'/api/participants/close_page/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                  },
                  body: JSON.stringify({
                    'uuid': localStorage.getItem('participant_uuid'),
                    'seconds': this.timeLimit - this.timePassed
                  })
                })
            }
        },
        created() {
            this.getQuestions();
            window.addEventListener(
              "beforeunload",
              this.leaving
            );
        }
    }
</script>

<style>
.picked-choice {
    background-color: #00415d;
    color: white;
    border-radius: 10px;
}
.choice-parent {
    display: table;
    height: 100%;
    overflow: hidden;
}
.choice-child {
    display: table-cell;
    width: 50000px;
    vertical-align: middle;
    margin: 0 auto;
    text-align: center;
}
a {
    text-decoration: none;
    color: #00415d;
}
</style>