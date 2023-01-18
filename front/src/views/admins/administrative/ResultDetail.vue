<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
            <br><b style="color: #00415d;">{{ info }}</b>
        </div>
        <div v-bind:class="[ContentClass]">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                type="button" @click="$router.push('/admin/results/participants?olympiad_id='+$route.query.olympiad_id)">
                Вернуться к списку участников
            </button>
            <h3 class="table-name" style="color: #00415d;">
                Ответы на вопросы олимпиады участника<br><b>{{ participantSurnameName }}</b>
            </h3>
            <button class="btn btn-lg btn-primary m-auto iohk-butt"
                type="button" @click="recountPoints();">
                <font-awesome-icon icon="fa-solid fa-calculator" /> Пересчитать баллы
            </button><br><br>
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
                            <div class="container-table" style="width: 65%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th colspan="3">Результат по вопросу</th>
                                            </tr>
                                            <tr>
                                                <th>Правильный ответ</th>
                                                <th>Ответ участника</th>
                                                <th>Баллы</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td><b>{{ getClassicCorrect(question[0]) }}</b></td>
                                                <td>
                                                    <b class="correct"
                                                        v-if="getClassicPoints(question[0]) !== 0">
                                                        {{ getClassicAnswer(question[0]) }}
                                                    </b>
                                                    <b class="wrong"
                                                        v-if="getClassicPoints(question[0]) === 0">
                                                        {{ getClassicAnswer(question[0]) }}
                                                    </b>
                                                </td>
                                                <td>
                                                    <input type="number" min="0" max="1" class="form-control text-center"
                                                        :value="getClassicPoints(question[0])"
                                                        @change="event => saveClassicDetail(event, question[0])">
                                                </td>
                                            </tr>
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
                                                <th colspan="4">Результат по вопросу</th>
                                            </tr>
                                            <tr>
                                                <th>Подпись к ответу</th>
                                                <th>Правильный ответ</th>
                                                <th>Ответ участника</th>
                                                <th>Баллы</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="rec in chunckedAcc(question[0])">
                                                <td><b>{{ rec[0] }}</b></td>
                                                <td><b>{{ rec[1] }}</b></td>
                                                <td>
                                                    <b class="correct"
                                                        v-if="rec[3] !== 0">
                                                        {{ rec[2] }}
                                                    </b>
                                                    <b class="wrong"
                                                        v-if="rec[3] === 0">
                                                        {{ rec[2] }}
                                                    </b>
                                                </td>
                                                <td>
                                                    <input type="number" class="form-control text-center"
                                                        min="0" max="1" :value="rec[3]"
                                                        @change="event => saveAccTableShort(event, question[0], rec[4])">
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
                                                <th colspan="2">Результат по вопросу</th>
                                            </tr>
                                            <tr>
                                                <th>Ответ участника</th>
                                                <th>Баллы</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>{{ getDetailedAnswer(question[0]) }}</td>
                                                <td>
                                                    <input type="number" class="form-control text-center"
                                                        min="0"
                                                        :value="getDetailedPoints(question[0])"
                                                        @change="event => saveClassicDetail(event, question[0])">
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
                                                <th colspan="4">Результат по вопросу</th>
                                            </tr>
                                            <tr>
                                                <th>Подпись к ответу</th>
                                                <th>Правильный ответ</th>
                                                <th>Ответ участника</th>
                                                <th>Баллы</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td><b>{{ getShortLabel(question[0]) }}</b></td>
                                                <td><b>{{ getShortCorrect(question[0]) }}</b></td>
                                                <td>
                                                    <b class="correct"
                                                        v-if="getShortPoints(question[0]) !== 0">
                                                        {{ getShortAnswer(question[0]) }}
                                                    </b>
                                                    <b class="wrong"
                                                        v-if="getShortPoints(question[0]) === 0">
                                                        {{ getShortAnswer(question[0]) }}
                                                    </b>
                                                </td>
                                                <td>
                                                    <input type="number" class="form-control text-center"
                                                        min="0" max="1" :value="getShortPoints(question[0])"
                                                        @change="event => saveAccTableShort(event, question[0], getShortAnswerId(question[0]))">
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
                                                <th colspan="5">Результат по вопросу</th>
                                            </tr>
                                            <tr>
                                                <th rowspan="2">Подпись к ответу</th>
                                                <th colspan="4">Информация об ответе</th>
                                            </tr>
                                            <tr>
                                                <th>Столбец</th>
                                                <th>Правильный ответ</th>
                                                <th>Ответ пользователя</th>
                                                <th>Баллы</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(row, index) in getRows(question[0])">
                                                <td class="rowspan" v-if="index % 2 == 0" :rowspan="getCountCols(question[0])">
                                                    <b>{{ row }}</b>
                                                </td>
                                                <td><b>{{ getCol(question[0], index) }}</b></td>
                                                <td>
                                                    <b>{{ getTableCorrect(question[0], getCol(question[0], index), row) }}</b>
                                                </td>
                                                <td>
                                                    <b class="correct"
                                                       v-if="getTablePoints(question[0], getCol(question[0], index), row) !== 0">
                                                        {{ getTableAnswer(question[0], getCol(question[0], index), row) }}
                                                    </b>
                                                    <b class="wrong"
                                                       v-if="getTablePoints(question[0], getCol(question[0], index), row) === 0">
                                                        {{ getTableAnswer(question[0], getCol(question[0], index), row) }}
                                                    </b>
                                                </td>
                                                <td>
                                                    <input type="number" class="form-control text-center"
                                                        min="0" max="1"
                                                        :value="getTablePoints(question[0], getCol(question[0], index), row)"
                                                        @change="event => saveAccTableShort(event, question[0], getTableAnswerId(question[0], getCol(question[0], index), row))">
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
        </div>
    </div>
</template>

<script>
    import Header from "../../../components/Header.vue"
    import AdminMenu from "../../../components/AdminMenu.vue"
    import OlympicGrid from "../../../components/OlympicGrid.vue"
    import ChoicesGrid from "../../../components/ChoicesGrid.vue"

    export default {
        name: "ResultDetail",
        components: {
            Header,
            AdminMenu,
            OlympicGrid,
            ChoicesGrid
        },
        data() {
            return {
                info: 'Формируем страницу с ответами...',
                even: 1,
                participantSurnameName: '',
                listQuestions: [],
                listClassicAnswers: [],
                listAccAnswers: [],
                listShortAnswers: [],
                listDetailedAnswers: [],
                listTableAnswers: [],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
            }
        },
        methods: {
            async getClassicAnswers() {
               let url = this.$store.state.backendUrl+'/api/service/result_get_classic/'+this.$route.query.identifier+'/'
               this.listClassicAnswers = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
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
            getClassicCorrect(question_id) {
                let label = ''
                $.each(this.listClassicAnswers, function(index, list) {
                    if (index == question_id) {
                       label = list[0]
                       return false
                    }
                })
                return label
            },
            getClassicAnswer(question_id) {
                let answer = ''
                $.each(this.listClassicAnswers, function(index, list) {
                    if (index == question_id) {
                       answer = list[1]
                       return false
                    }
                })
                return answer
            },
            getClassicPoints(question_id) {
                let points = ''
                $.each(this.listClassicAnswers, function(index, list) {
                    if (index == question_id) {
                       points = list[2]
                       return false
                    }
                })
                return points
            },
            async getAccAnswers() {
               let url = this.$store.state.backendUrl+'/api/service/result_get_acc/'+this.$route.query.identifier+'/'
               this.listAccAnswers = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
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
            chunckedAcc(question_id) {
                const result = []
                $.each(this.listAccAnswers, function(index, chs) {
                    if (index == question_id) {
                        for (let i = 0; i < chs.length; i += 5) {
                            result.push(chs.slice(i, i + 5))
                        }
                    }
                })
                return result
            },
            async getShortAnswers() {
               let url = this.$store.state.backendUrl+'/api/service/result_get_short/'+this.$route.query.identifier+'/'
               this.listShortAnswers = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
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
            getShortLabel(question_id) {
                let label = ''
                $.each(this.listShortAnswers, function(index, list) {
                    if (index == question_id) {
                       label = list[0]
                       return false
                    }
                })
                return label
            },
            getShortCorrect(question_id) {
                let correct = ''
                $.each(this.listShortAnswers, function(index, list) {
                    if (index == question_id) {
                       correct = list[1]
                       return false
                    }
                })
                return correct
            },
            getShortAnswer(question_id) {
                let answer = ''
                $.each(this.listShortAnswers, function(index, list) {
                    if (index == question_id) {
                       answer = list[2]
                       return false
                    }
                })
                return answer
            },
            getShortPoints(question_id) {
                let points = ''
                $.each(this.listShortAnswers, function(index, list) {
                    if (index == question_id) {
                       points = list[3]
                       return false
                    }
                })
                return points
            },
            getShortAnswerId(question_id) {
                let answer_id = ''
                $.each(this.listShortAnswers, function(index, list) {
                    if (index == question_id) {
                       answer_id = list[4]
                       return false
                    }
                })
                return answer_id
            },
            async getDetailedAnswers() {
               let url = this.$store.state.backendUrl+'/api/service/result_get_detailed/'+this.$route.query.identifier+'/'
               this.listDetailedAnswers = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
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
            getDetailedAnswer(question_id) {
                let answer = ''
                $.each(this.listDetailedAnswers, function(index, list) {
                    if (index == question_id) {
                       answer = list[0]
                       return false
                    }
                })
                return answer
            },
            getDetailedPoints(question_id) {
                let points = ''
                $.each(this.listDetailedAnswers, function(index, list) {
                    if (index == question_id) {
                       points = list[1]
                       return false
                    }
                })
                return points
            },
            async getTableAnswers() {
               let url = this.$store.state.backendUrl+'/api/service/result_get_table/'+this.$route.query.identifier+'/'
               this.listTableAnswers = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
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
            getCols(question_id){
                let cols = []
                let check = []
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, val) {
                            cols.push(i_col)
                        })
                        return false
                    }
                })
                return cols
            },
            getCountCols(question_id) {
                let arr = this.getCols(question_id)
                return arr.length
            },
            getIndexCols(question_id, index) {
                let count = this.getCountCols(question_id)
                if (index % count == 0) {
                    return 0
                } else {
                    return index % count
                }
            },
            getCol(question_id, index) {
                return this.getCols(question_id)[this.getIndexCols(question_id, index)]
            },
            getRows(question_id) {
                let rows = []
                let check = []
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, row) {
                            $.each(row, function(i_row, list) {
                                if (!(check.includes(i_row))) {
                                    check.push(i_row)
                                    rows.push(i_row)
                                    rows.push(i_row)
                                }
                            })
                        })
                        return false
                    }
                })
                return rows
            },
            getTableCorrect(question_id, form_col, form_row) {
                let correct = []
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, row) {
                            if (i_col == form_col) {
                               $.each(row, function(i_row, list) {
                                    if (i_row == form_row) {
                                        correct = list[0]
                                        return false
                                    }
                                })
                            }
                        })
                    }
                })
                return correct
            },
            getTableAnswer(question_id, form_col, form_row) {
                let answer = ''
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, row) {
                            if (i_col == form_col) {
                               $.each(row, function(i_row, list) {
                                    if (i_row == form_row) {
                                        answer = list[1]
                                        return false
                                    }
                                })
                            }
                        })
                    }
                })
                return answer
            },
            getTablePoints(question_id, form_col, form_row) {
                let points = ''
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, row) {
                            if (i_col == form_col) {
                               $.each(row, function(i_row, list) {
                                    if (i_row == form_row) {
                                        points = list[2]
                                        return false
                                    }
                                })
                            }
                        })
                    }
                })
                return points
            },
            getTableAnswerId(question_id, form_col, form_row) {
                let answer_id = ''
                $.each(this.listTableAnswers, function(index, col){
                    if (index == question_id) {
                        $.each(col, function(i_col, row) {
                            if (i_col == form_col) {
                               $.each(row, function(i_row, list) {
                                    if (i_row == form_row) {
                                        answer_id = list[3]
                                        return false
                                    }
                                })
                            }
                        })
                    }
                })
                return answer_id
            },
            async saveClassicDetail(e, question_id) {
                await fetch(this.$store.state.backendUrl+'/api/service/result_save_classic_detail/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                  body: JSON.stringify({
                    'identifier': this.$route.query.identifier,
                    'question_id': question_id,
                    'points':e.target.value,
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json().then(data => {
                        showBanner('.banner.success', data.success)
                        return false
                      })
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            async saveAccTableShort(e, question_id, answer_id) {
                await fetch(this.$store.state.backendUrl+'/api/service/result_save_acc_table_short/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                  body: JSON.stringify({
                    'identifier': this.$route.query.identifier,
                    'question_id': question_id,
                    'answer_id': answer_id,
                    'points':e.target.value,
                  })
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json().then(data => {
                        showBanner('.banner.success', data.success)
                        return false
                      })
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            async recountPoints() {
                let url = this.$store.state.backendUrl+'/api/service/result_recount/'+this.$route.query.identifier+'/'
                await fetch(url, {
                  method: 'GET',
                  headers: {
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  }
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json().then(data => {
                        showBanner('.banner.success', data.success)
                        return false
                      })
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
            },
            async getLastFirstName() {
                let url = this.$store.state.backendUrl+'/api/service/result_get_lastfirstname/'+this.$route.query.identifier+'/'
                let response = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
                this.participantSurnameName = response.success
            },
            async getQuestions() {
               let url = this.$store.state.backendUrl+'/api/service/result_questions/'+this.$route.query.identifier+'/'
               this.listQuestions = await fetch(url, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
               .then(resp => {
                  if (resp.status == 200) {
                      return resp.json()
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     return false
                  }
                })
                this.getLastFirstName()
                this.getClassicAnswers()
                this.getAccAnswers()
                this.getShortAnswers()
                this.getDetailedAnswers()
                this.getTableAnswers()
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
        },
        created() {
            this.getQuestions()
        }
    }
</script>

<style>
.correct {
    color: green;
}
.wrong {
    color: red;
}
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