<template>
    <Header />
    <QuestionMenu />
     <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Ответы (тип вопроса: <b>{{ question.type }}</b>)<br>
                <button class="btn btn-lg btn-primary m-auto iohk-butt"
                    type="button" @click="showQuestion();">
                    Показать вопрос
                </button>
             </h3><br>
            <AnswerGrid>
                 <template v-slot:a-main>
                    <div class="half-block">
                        <div v-if="question.type == 'Табличный'">
                            <div v-bind:class="[LoadClass]">
                                <img src="../../../assets/gifs/load.gif">
                            </div>
                            <div v-bind:class="[ContentClass]">
                                <b class="table-name" style="color: #00415d;">
                                    Заголовки столбцов в таблице ответов
                                 </b><br>
                                     <a href="#" @click = "addColumnSidebox();">
                                        <div style="display: inline;">
                                            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                                type="button">
                                                <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить
                                            </button>
                                        </div>
                                    </a>
                                <div class="container-table" style="width: 100%;">
                                    <div class="table-wrapper">
                                        <table class="fl-table">
                                            <thead>
                                                <tr>
                                                    <th>Порядковый номер</th>
                                                    <th>Наименование столбца</th>
                                                    <th>Удалить</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="column in listColumns">
                                                    <td>{{ column.seq_number }}</td>
                                                    <td class="no-wrap">
                                                        {{ column.column }}
                                                    </td>
                                                    <td>
                                                        <a href="#" @click = "deleteColumn(column.id);" style="color: #00415d;">
                                                            <font-awesome-icon icon="fa-solid fa-trash" />
                                                        </a>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="question.type == 'Развернутый ответ'">
                            <b>Развернутый ответ, участнику необходимо заполнить
                            расширенное текстовое поле для ответа.<br> Проверка осуществляется в ручном режиме</b>
                        </div>
                        <div v-if="question.type == 'Краткий ответ'">
                           <div v-bind:class="[LoadClass]">
                                <img src="../../../assets/gifs/load.gif">
                           </div>
                           <div v-bind:class="[ContentClass]">
                                <b class="table-name" style="color: #00415d;">
                                    Информация о кратком ответе
                                </b>
                                <div class="container-table" style="width: 100%;">
                                    <div class="table-wrapper">
                                        <table class="fl-table">
                                            <thead>
                                                <tr>
                                                    <th>Подпись к полю ответа</th>
                                                    <th>Правильный ответ</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <input type="text" class="form-control text-center"
                                                            ref="signature"
                                                            :value="shortAnswer.label"
                                                            @change="event => setShortSignature(event)">
                                                    </td>
                                                    <td>
                                                        <input type="text" class="form-control text-center"
                                                            ref="correct"
                                                            :value="shortAnswer.short_correct"
                                                            @change="event => setShortCorrect(event)">
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                           </div>
                        </div>
                        <div v-if="question.type == 'Соответствие'">
                            <div v-bind:class="[LoadClass]">
                                <img src="../../../assets/gifs/load.gif">
                            </div>
                            <div v-bind:class="[ContentClass]">
                                <b class="table-name" style="color: #00415d;">
                                    Варианты ответов
                                 </b><br>
                                     <a href="#" @click = "addAccSidebox();">
                                        <div style="display: inline;">
                                            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                                type="button">
                                                <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить вариант
                                            </button>
                                        </div>
                                    </a>
                                <div class="container-table" style="width: 100%;">
                                    <div class="table-wrapper">
                                        <table class="fl-table">
                                            <thead>
                                                <tr>
                                                    <th>Вариант</th>
                                                    <th>Удалить</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="acc in listAccs">
                                                    <td class="no-wrap">
                                                        {{ acc.value }}
                                                    </td>
                                                    <td>
                                                        <a href="#" @click = "deleteAcc(acc.id);" style="color: #00415d;">
                                                            <font-awesome-icon icon="fa-solid fa-trash" />
                                                        </a>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="question.type == 'Классический'">
                            <div v-bind:class="[LoadClass]">
                                <img src="../../../assets/gifs/load.gif">
                            </div>
                            <div v-bind:class="[ContentClass]">
                                <b class="table-name" style="color: #00415d;">
                                    Варинты ответа
                                 </b><br>
                                     <a href="#" @click = "addChoiceSidebox();">
                                        <div style="display: inline;">
                                            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                                type="button">
                                                <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить вариант
                                            </button>
                                        </div>
                                    </a>
                                <div class="container-table" style="width: 100%;">
                                    <div class="table-wrapper">
                                        <table class="fl-table">
                                            <thead>
                                                <tr>
                                                    <th>Вариант ответа</th>
                                                    <th>Прваильный ответ</th>
                                                    <th>Удалить</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="choice in listChoices">
                                                    <td class="no-wrap">
                                                        {{ choice.choice }}
                                                    </td>
                                                    <td>
                                                        <div v-if="choice.correct == false">
                                                            Нет&nbsp;<a href="#" @click = "setCorrectChoice(choice.id);" style="color: #00415d;">
                                                                <font-awesome-icon icon="fa-solid fa-check" />
                                                            </a>
                                                        </div>
                                                        <div v-if="choice.correct == true">
                                                            Да
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <a href="#" @click = "deleteChoice(choice.id, choice.correct);" style="color: #00415d;">
                                                            <font-awesome-icon icon="fa-solid fa-trash" />
                                                        </a>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                 </template>
                 <template v-slot:a-additional v-if="question.type == 'Табличный'">
                    <div>
                        <div v-bind:class="[LoadClass]">
                            <img src="../../../assets/gifs/load.gif">
                        </div>
                        <div v-bind:class="[ContentClass]">
                            <b class="table-name" style="color: #00415d;">
                                Таблица ответов
                            </b><br>
                            <a href="#" @click = "addRowSidebox();">
                                <div style="display: inline;">
                                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button">
                                        <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить строку
                                    </button>
                                </div>
                            </a>
                            <div class="container-table" style="width: 100%;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th>Порядковый номер</th>
                                                <th>Ответы\Столбцы</th>
                                                <th v-for="column in listColumns">
                                                    {{ column.column }}
                                                </th>
                                                <th>Удалить</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="row in listRows">
                                                <td>{{ row.seq_number }}</td>
                                                <td>{{ row.label }}</td>
                                                <td v-for="column in listColumns">
                                                    <input type="text" class="form-control text-center"
                                                        :id="`answer_${row.id}_${column.id}`"
                                                        :value="getAnswer(row.label, column.id)"
                                                        @change="event => setAnswer(event, row.label, column.id)">
                                                </td>
                                                <td>
                                                    <a href="#" @click = "deleteRow(row.label);" style="color: #00415d;">
                                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                                    </a>&nbsp;&nbsp;&nbsp;
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                 </template>
                 <template v-slot:a-additional v-if="question.type == 'Соответствие'">
                    <div>
                        <div v-bind:class="[LoadClass]">
                            <img src="../../../assets/gifs/load.gif">
                        </div>
                        <div v-bind:class="[ContentClass]">
                            <b class="table-name" style="color: #00415d;">
                                Соответствие вариантов ответов
                            </b><br>
                            <a href="#" @click = "addAccRowSidebox();">
                                <div style="display: inline;">
                                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                        type="button">
                                        <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить строку
                                    </button>
                                </div>
                            </a>
                            <div class="container-table" style="width: 50%; margin: 0 auto;">
                                <div class="table-wrapper">
                                    <table class="fl-table">
                                        <thead>
                                            <tr>
                                                <th>Подпись к ответу</th>
                                                <th>Вариант ответа</th>
                                                <th>Удалить</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="row in listAccRows">
                                                <td>{{ row.label }}</td>
                                                <td>{{ row.acc_correct }}</td>
                                                <td>
                                                    <a href="#" @click = "deleteAccRow(row.id);" style="color: #00415d;">
                                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                                    </a>&nbsp;&nbsp;&nbsp;
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                 </template>
            </AnswerGrid><br>
            <button class="btn btn-lg btn-primary m-auto iohk-butt"
                type="button" @click="goToQuestions();">
                Сохранить
            </button>
        </div>
    </div>
    <ModalAdmin v-show="showModal" @close-modal="showModal = false">
        <template v-slot:main-info>
            <editor
               v-model="question_mce"
               api-key="p0t8lf7pix6acnxfbd8i3ako0vo4ke98tll8pe4mufqr1hcw"
               :disabled=true
               toolbar=false
               :init="{
                 height: 750,
                 menubar: false,
                 language: 'ru',
                 resize: 'true'
               }"
            />
        </template>
    </ModalAdmin>
    <SideBox>
        <template v-slot:side-chb>
            <input type="checkbox" id="side-checkbox" v-model="SideBoxChecked"/>
        </template>
        <template v-slot:sidebox-title>
            <p v-bind:class="[AddColumnClass]">Новый столбец</p>
            <p v-bind:class="[AddRowClass]">Новая строка ответов</p>
            <p v-bind:class="[AddChoiceClass]">Новый вариант ответа</p>
            <p v-bind:class="[AddAccClass]">Новый вариант ответа</p>
            <p v-bind:class="[AddAccRowClass]">Новая строка ответа</p>
        </template>
        <template v-slot:main-table-trs>
            <tr v-if="AddColumnClass === 'sidebox-active'">
                <td>
                    <center>Порядковый номер: </center>
                </td>
                <td>
                    <input type="number" class="form-control text-center" ref="addColumnNumber">
                </td>
            </tr>
            <tr v-if="AddColumnClass === 'sidebox-active'">
                <td>
                    <center>Наименование столбца: </center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="addColumn">
                </td>
            </tr>
            <tr v-if="AddRowClass === 'sidebox-active'">
                <td>
                    <center>Порядковый номер: </center>
                </td>
                <td>
                    <input type="number" class="form-control text-center" ref="addRowNumber">
                </td>
            </tr>
            <tr v-if="AddRowClass === 'sidebox-active'">
                <td>
                    <center>Подпись к строке ответа: </center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="addRow">
                </td>
            </tr>
            <tr v-if="AddChoiceClass === 'sidebox-active'">
                <td>
                    <center>Вариант ответа: </center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="addChoice">
                </td>
            </tr>
            <tr v-if="AddAccClass === 'sidebox-active'">
                <td>
                    <center>Вариант ответа: </center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="addAcc">
                </td>
            </tr>
            <tr v-if="AddChoiceClass === 'sidebox-active'">
                <td>
                    <center>Правильный ответ: </center>
                </td>
                <td>
                    <input type="checkbox" v-model="ChoiceCorrect">
                </td>
            </tr>
            <tr v-if="AddAccRowClass === 'sidebox-active'">
                <td>
                    <center>Подпись к ответу: </center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="addAccRowLabel">
                </td>
            </tr>
            <tr v-if="AddAccRowClass === 'sidebox-active'">
                <td>
                    <center>Правильный ответ: </center>
                </td>
                <td>
                    <select class="form-control text-center" v-model="addAccRowValue">
                        <option v-for="value in listAccs" :value="value.id">
                            {{ value.value }}
                        </option>
                    </select>
                </td>
            </tr>
        </template>
        <template v-slot:sidebox-button>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../../../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[AddColumnClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddColumnClass]"
                        type="button" @click="addColumnFunction();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[AddRowClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddRowClass]"
                        type="button" @click="addRowFunction();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[AddChoiceClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddChoiceClass]"
                        type="button" @click="addChoiceFunction();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[AddAccClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddAccClass]"
                        type="button" @click="addAccFunction();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[AddAccRowClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddAccRowClass]"
                        type="button" @click="addAccRowFunction();">
                        Добавить
                    </button>
                </div>
            </div>
        </template>
    </SideBox>
</template>

<script>
    import Header from "../../../components/Header.vue"
    import SideBox from "../../../components/SideBox.vue"
    import AnswerGrid from "../../../components/AnswerGrid.vue"
    import QuestionMenu from "../../../components/QuestionMenu.vue"
    import ModalAdmin from '../../../components/ModalAdmin.vue'
    import Editor from '@tinymce/tinymce-vue'

    export default {
        name: "Answers",
        components: {
            SideBox,
            Header,
            QuestionMenu,
            AnswerGrid,
            ModalAdmin,
            'editor': Editor
        },
        data() {
            return {
                SideBoxChecked: false,
                shortAnswer: [],
                question: [],
                cellAnswers: [],
                listChoices: [],
                listAccs: [],
                listAccRows: [],
                listColumns: [],
                listRows: [],
                listLevels: [],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                AddColumnClass: 'sidebox-deactive',
                AddRowClass: 'sidebox-deactive',
                AddChoiceClass: 'sidebox-deactive',
                AddAccClass: 'sidebox-deactive',
                AddAccRowClass: 'sidebox-deactive',
                ButtonClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                showModal: false,
            }
        },
        methods: {
            getAnswer(row_label, col_id) {
                return this.cellAnswers[row_label+'-'+col_id]
            },
            async setAnswer(event, row_label, col_id) {
                await fetch(this.$store.state.backendUrl+'/api/service/set_answer/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                  },
                  body: JSON.stringify({
                    'label': row_label,
                    'column_id':col_id,
                    'correct': event.target.value
                  })
                })
                .then(resp => resp.json())
                .then(data => {
                    if (data.error) {
                        showBanner('.banner.error', data.error)
                        return false
                    } else {
                        showBanner('.banner.success', data.success)
                        this.getQuestionType()
                    }
                })
            },
            async setShortSignature(event) {
                await fetch(this.$store.state.backendUrl+'/api/service/short_signature/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                  },
                  body: JSON.stringify({
                    'question_id': this.question.id,
                    'label': event.target.value
                  })
                })
                .then(resp => resp.json())
                .then(data => {
                    if (data.error) {
                        showBanner('.banner.error', data.error)
                        return false
                    } else {
                        showBanner('.banner.success', data.success)
                        this.getQuestionType()
                    }
                })
            },
            async setShortCorrect(event) {
                await fetch(this.$store.state.backendUrl+'/api/service/short_correct/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                  },
                  body: JSON.stringify({
                    'question_id': this.question.id,
                    'correct': event.target.value
                  })
                })
                .then(resp => resp.json())
                .then(data => {
                    if (data.error) {
                        showBanner('.banner.error', data.error)
                        return false
                    } else {
                        showBanner('.banner.success', data.success)
                        this.getQuestionType()
                    }
                })
            },
            async getCellAnswers(question_id) {
                this.cellAnswers = await fetch(this.$store.state.backendUrl+'/api/service/answers/', {
                  method: 'POST',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                  },
                  body: JSON.stringify({
                    'question_id': question_id,
                  })
                })
                .then(resp => resp.json())
                .then(data => {
                    return data.success
                })
            },
            async getColumns(question_id){
                this.listColumns = await fetch(this.$store.state.backendUrl+'/api/service/question_columns?question='+question_id, {
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
            async getRows(question_id){
                this.listRows = await fetch(this.$store.state.backendUrl+'/api/service/question_rows?question='+question_id, {
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
            addRowSidebox() {
                this.AddRowClass = 'sidebox-active'
                this.AddAccClass = 'sidebox-deactive'
                this.AddAccRowClass = 'sidebox-deactive'
                this.AddColumnClass = 'sidebox-deactive'
                this.AddChoiceClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            checkRowExist(value) {
                let ex = false
                $.each(this.listRows, function(index, row){
                    if (row['label'] == value) {
                        ex = true
                    }
                })
                return ex
            },
            async addRowFunction() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addRowNumber.value == '') {
                    showBanner('.banner.error', 'Поле "Порядковый номер" не может быть пустым')
                } else if (this.$refs.addRow.value == '') {
                    showBanner('.banner.error', 'Поле "Подпись к строке ответа" не может быть пустым')
                } else if (this.checkRowExist(this.$refs.addRow.value)) {
                    showBanner('.banner.error', 'Такая строка уже существует')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/row_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question': this.question.id,
                        'label': this.$refs.addRow.value,
                        'seq_number': this.$refs.addRowNumber.value
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            this.ButtonClass = 'sidebox-active'
                            this.ButtonLoadClass = 'sidebox-deactive'
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getRows(this.question.id)
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async deleteRow(row_label){
                if (confirm('Вы действительно хотите удалить строку для ответов?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/row_delete/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question_id': this.question.id,
                        'label': row_label,
                      })
                    })
                    .then(resp => resp.json())
                    if (del.error){
                        showBanner('.banner.error', del.error)
                        return false
                    } else {
                        showBanner('.banner.success', del.success);
                        this.getQuestionType();
                    }

                }
            },
            addColumnSidebox() {
                this.AddColumnClass = 'sidebox-active'
                this.AddAccClass = 'sidebox-deactive'
                this.AddAccRowClass = 'sidebox-deactive'
                this.AddRowClass = 'sidebox-deactive'
                this.AddChoiceClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async addColumnFunction() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addColumn.value == '') {
                    showBanner('.banner.error', 'Поле "Наименование столбца" не может быть пустым')
                } else if (this.$refs.addColumnNumber.value == '') {
                    showBanner('.banner.error', 'Поле "Порядковый номер" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/column_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question': this.question.id,
                        'column': this.$refs.addColumn.value,
                        'seq_number': this.$refs.addColumnNumber.value
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            this.ButtonClass = 'sidebox-active'
                            this.ButtonLoadClass = 'sidebox-deactive'
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getColumns(this.question.id)
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async deleteColumn(column_id){
                if (confirm('Вы действительно хотите удалить заголовок?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/column_delete/'+column_id+'/', {
                      method: 'delete',
                      headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token'),
                      }
                    })
                    .then(resp => resp.json())
                    if (del.error){
                        showBanner('.banner.error', del.error)
                        return false
                    } else {
                        showBanner('.banner.success', del.success);
                        this.getQuestionType();
                    }

                }
            },
            addChoiceSidebox() {
                this.AddChoiceClass = 'sidebox-active'
                this.AddAccClass = 'sidebox-deactive'
                this.AddRowClass = 'sidebox-deactive'
                this.AddAccRowClass = 'sidebox-deactive'
                this.AddColumnClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async setCorrectChoice(choice_id) {
                const del = await fetch(this.$store.state.backendUrl+'/api/service/set_choice/', {
                  method: 'PUT',
                  headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                  },
                  body: JSON.stringify({
                    'question': this.question.id,
                    'choice_id': choice_id,
                  })
                })
                .then(resp => resp.json())
                if (del.error){
                    showBanner('.banner.error', del.error)
                    return false
                } else {
                    showBanner('.banner.success', del.success);
                    this.getQuestionType();
                }
            },
            async addChoiceFunction() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addChoice.value == '') {
                    showBanner('.banner.error', 'Поле "Вариант ответа" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/choice_add/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question': this.question.id,
                        'choice': this.$refs.addChoice.value,
                        'correct': this.ChoiceCorrect,
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            this.ButtonClass = 'sidebox-active'
                            this.ButtonLoadClass = 'sidebox-deactive'
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getChoices()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async deleteChoice(choice_id, check_correct) {
                if (check_correct) {
                    showBanner('.banner.error', 'Невозможно удалить правильный вариант ответа')
                        return false
                } else {
                    if (confirm('Вы действительно хотите удалить вариант ответа?')){
                        const del = await fetch(this.$store.state.backendUrl+'/api/service/choice_delete/'+choice_id+'/', {
                          method: 'delete',
                          headers: {
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Authorization': 'Token '+localStorage.getItem('access_token'),
                          }
                        })
                        .then(resp => resp.json())
                        if (del.error){
                            showBanner('.banner.error', del.error)
                            return false
                        } else {
                            showBanner('.banner.success', del.success);
                            this.getQuestionType();
                        }

                    }
                }
            },
            async getShortAnswer() {
                await fetch(this.$store.state.backendUrl+'/api/service/get_short?question_id='+this.$route.query.question_id, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.shortAnswer = data.success
                    } else {
                        showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                        return false
                    }
                })
            },
            async getChoices() {
                this.listChoices = await fetch(this.$store.state.backendUrl+'/api/service/choices?question_id='+this.$route.query.question_id, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(response => {
                    if (response.status == 200) {
                        return response.json()
                    } else {
                        showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                        return false
                    }
                })
            },
            async getAccs() {
                this.listAccs = await fetch(this.$store.state.backendUrl+'/api/service/accs?question_id='+this.$route.query.question_id, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(response => {
                    if (response.status == 200) {
                        return response.json()
                    } else {
                        showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                        return false
                    }
                })
            },
            async getAccRows() {
                this.listAccRows = await fetch(this.$store.state.backendUrl+'/api/service/acc_answers?question_id='+this.$route.query.question_id, {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(response => {
                    if (response.status == 200) {
                        return response.json()
                    } else {
                        showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                        return false
                    }
                })
            },
            addAccSidebox() {
                this.AddAccClass = 'sidebox-active'
                this.AddChoiceClass = 'sidebox-deactive'
                this.AddAccRowClass = 'sidebox-deactive'
                this.AddRowClass = 'sidebox-deactive'
                this.AddColumnClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            addAccRowSidebox() {
                this.AddAccClass = 'sidebox-deactive'
                this.AddChoiceClass = 'sidebox-deactive'
                this.AddAccRowClass = 'sidebox-active'
                this.AddRowClass = 'sidebox-deactive'
                this.AddColumnClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async deleteAcc(acc_id) {
                if (confirm('Вы действительно хотите удалить вариант ответа?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/acc_delete/'+acc_id+'/', {
                      method: 'delete',
                      headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token'),
                      }
                    })
                    .then(resp => resp.json())
                    if (del.error){
                        showBanner('.banner.error', del.error)
                        return false
                    } else {
                        showBanner('.banner.success', del.success);
                        this.getQuestionType();
                    }

                }
            },
            async deleteAccRow(row_id) {
                if (confirm('Вы действительно хотите удалить строку ответа?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/acc_answer_delete/'+row_id+'/', {
                      method: 'delete',
                      headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token'),
                      }
                    })
                    .then(resp => resp.json())
                    if (del.error){
                        showBanner('.banner.error', del.error)
                        return false
                    } else {
                        showBanner('.banner.success', del.success);
                        this.getQuestionType();
                    }

                }
            },
            checkExistAcc() {
                let origin = true
                let val = this.$refs.addAccRowLabel.value
                $.each(this.listAccRows, function(index, row)  {
                    if (row.label == val) {
                        origin = false
                        return false
                    }
                })
                return origin
            },
            async addAccFunction() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addAcc.value == '') {
                    showBanner('.banner.error', 'Поле "Вариант ответа" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/acc_add/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question': this.question.id,
                        'value': this.$refs.addAcc.value,
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            this.ButtonClass = 'sidebox-active'
                            this.ButtonLoadClass = 'sidebox-deactive'
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getQuestionType()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async addAccRowFunction() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                this.checkExistAcc()
                if (this.$refs.addAccRowLabel.value == '') {
                    showBanner('.banner.error', 'Поле "Подпись к ответу" не может быть пустым')
                } else if (this.$refs.addAccRowLabel.value == '') {
                    showBanner('.banner.error', 'Поле "Подпись к ответу" не может быть пустым')
                } else if (!(this.checkExistAcc())) {
                    showBanner('.banner.error', 'Строка с такой подписью уже существует')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/acc_answer_add/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'question': this.question.id,
                        'label': this.$refs.addAccRowLabel.value,
                        'acc_correct': this.addAccRowValue
                      })
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            this.ButtonClass = 'sidebox-active'
                            this.ButtonLoadClass = 'sidebox-deactive'
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getQuestionType()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async getQuestionType(){
                await fetch(this.$store.state.backendUrl+'/api/service/question/'+this.$route.query.question_id+'/', {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                })
                .then(response => {
                    if (response.status == 200) {
                        return response.json()
                    } else {
                        showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                        return false
                    }
                })
                .then(data => {
                    this.question = data
                    this.question_mce = data['question']
                    if (data.type == 'Табличный') {
                        this.getCellAnswers(data.id)
                        this.getColumns(data.id)
                        this.getRows(data.id)
                    } else if (data.type == 'Краткий ответ') {
                        this.getShortAnswer()
                    } else if (data.type == 'Классический') {
                        this.getChoices()
                    } else if (data.type == 'Соответствие') {
                        this.getAccs()
                        this.getAccRows()
                    } else {

                    }
                })
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            showQuestion() {
                this.showModal = true
            },
            goToQuestions() {
                showBanner('.banner.success', 'Вопрос успешно сохранен');
                this.$router.push('/admin/questions')
            },
        },
        created() {
            this.getQuestionType()
        }
    }
</script>

<style>
.half-block{
    margin: 0 auto;
    width: 50%;
    margin-bottom: 5px;
}
</style>