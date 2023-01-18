<template>
    <Header />
    <QuestionMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Вопросы
             </h3><br>
                <router-link class="nav-href" to="/admin/new_question">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить
                        </button>
                    </div>
                </router-link>&nbsp;
                <a href="#" @click = "findSidebox();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-magnifying-glass" :style="{ color: white }"/>&nbsp;Поиск
                        </button>
                    </div>
                </a>
            <br><br>
            <div class="container-table" style="width: 95vw;">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th>
                                    Дата создания <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('date_create');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Тема вопроса <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('level');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Тип вопроса <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('type');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th style="width: 50%;">
                                    Формулировка вопроса
                                </th>
                                <th>Ответы</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="question in listQuestions">
                                <td class="no-wrap">
                                    {{ question.date_create }}
                                </td>
                                <td>{{ question.level }} </td>
                                <td class="no-wrap">{{ question.type }}</td>
                                <td v-html="question.question"></td>
                                <td>
                                    <a :href="'/admin/answers?question_id=' + question.id" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-eye" />
                                    </a>
                                </td>
                                <td class="no-wrap">
                                    <a href="#" @click = "deleteQuestion(question.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a :href="'/admin/edit_question?question_id=' + question.id" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <SideBox>
        <template v-slot:side-chb>
            <input type="checkbox" id="side-checkbox" v-model="SideBoxChecked"/>
        </template>
        <template v-slot:sidebox-title>
            <p v-bind:class="[FindClass]">Поиск вопросов</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Дата добавления вопроса:</center>
                </td>
                <td>
                    <input type="date" class="form-control text-center" ref="findDateCreate">
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Тема вопроса:</center>
                </td>
                <td>
                    <select class="form-control text-center" v-model="findLevel">
                        <option v-for="level in listLevels" :value="level.id">
                            {{ level.level }}
                        </option>
                    </select>
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Тип вопроса:</center>
                </td>
                <td>
                    <select class="form-control text-center" v-model="findTypes">
                        <option v-for="type in listTypes">
                            {{ type }}
                        </option>
                    </select>
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Формулировка вопроса:</center>
                </td>
                <td>
                    <textarea class="form-control" v-model="findQuestion">
                    </textarea>
                </td>
            </tr>
        </template>
        <template v-slot:sidebox-button>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../../../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[FindClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                        type="button" @click="findQuestions();">
                        Поиск
                    </button>
                </div>
            </div>
        </template>
    </SideBox>
</template>

<script>
    import Header from "../../../components/Header.vue"
    import SideBox from "../../../components/SideBox.vue"
    import QuestionMenu from "../../../components/QuestionMenu.vue"
    import Editor from '@tinymce/tinymce-vue'

    export default {
        name: "Questions",
        components: {
            Header,
            QuestionMenu,
            SideBox,
            'editor': Editor
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                ButtonClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listQuestions:[],
                listLevels:[],
                listTypes:['Классический', 'Соответствие', 'Табличный', 'Развернутый ответ', 'Краткий ответ'],
                editLevelObj:[],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                sort: '-date_create'
            }
        },
        methods: {
            sorted(obj) {
                if (this.sort == obj) {
                    this.sort = "-"+obj
                } else {
                    this.sort = obj
                }
                this.getQuestions();
            },
            async getLevels() {
                this.listLevels = await fetch(this.$store.state.backendUrl+'/api/service/levels/', {
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
            async getQuestions() {
                let url = ''
                if (this.$route.query.level) {
                    url = this.$store.state.backendUrl+'/api/service/questions?ordering='+this.sort+'&level='+this.$route.query.level
                } else if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/service/questions?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/questions?ordering='+this.sort
                }
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
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            findSidebox() {
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async findQuestions() {
                if (this.$refs.findDateCreate.value != '') {
                    this.findString = 'date_create='+this.$refs.findDateCreate.value+'&'
                }
                if (this.findLevel != null) {
                    this.findString = 'level='+this.findLevel+'&'
                }
                if (this.findTypes != null) {
                    this.findString = 'type='+this.findTypes+'&'
                }
                if (this.findQuestion != null) {
                    this.findString = 'question='+this.findQuestion+'&'
                }
                this.getQuestions()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
            async deleteQuestion(question_id) {
                if (confirm('Вы действительно хотите удалить вопрос?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/question_delete/'+question_id+'/', {
                      method: 'DELETE',
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
                        this.getQuestions();

                    }
                }
            }
        },
        created() {
            this.getQuestions()
            this.getLevels()
        }
    }
</script>

<style>

</style>