<template>
    <Header />
    <QuestionMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Темы вопросов
             </h3><br>
                <a href="#" @click = "addSidebox();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить
                        </button>
                    </div>
                </a>&nbsp;
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
                                    Наименование<br>темы <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('level');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Количество вопросов</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="level in listLevels">
                                <td class="no-wrap">
                                    {{ level.date_create }}<br>
                                </td>
                                <td>{{ level.level }}</td>
                                <td>
                                    <div v-if="level.question_count > 0">
                                        <router-link :to="'/admin/questions?level='+level.id">
                                            {{ level.question_count }}
                                        </router-link>
                                    </div>
                                    <div v-if="level.question_count === 0">
                                       -
                                    </div>
                                </td>
                                <td class="no-wrap">
                                    <a href="#" @click = "deleteLevel(level.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a href="#" @click = "editSideboxLevel(level.id);" style="color: #00415d;">
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
            <p v-bind:class="[FindClass]">Поиск тем вопросов</p>
            <p v-bind:class="[EditClass]">Изменение темы вопроса</p>
            <p v-bind:class="[AddClass]">Новая тема вопросов</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Дата добавления темы:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="date" class="form-control text-center" ref="addDateCreate" disabled>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="date" class="form-control text-center" ref="editDateCreate" disabled>
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="date" class="form-control text-center" ref="findDateCreate">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Наименование темы:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="text" class="form-control text-center" ref="addLevel">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editLevel">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findLevel">
                </td>
            </tr>
        </template>
        <template v-slot:sidebox-button>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../../../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[EditClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditClass]"
                        type="button" @click="editLevelFunc();">
                        Изменить
                    </button>
                </div>
                <div v-bind:class="[FindClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                        type="button" @click="findLevels();">
                        Поиск
                    </button>
                </div>
                <div v-bind:class="[AddClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddClass]"
                        type="button" @click="newLevel();">
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
    import QuestionMenu from "../../../components/QuestionMenu.vue"

    export default {
        name: "QuestionLevels",
        components: {
            Header, QuestionMenu, SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                ButtonClass: 'sidebox-deactive',
                EditClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                AddClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listLevels:[],
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
                this.getLevels();
            },
            async getLevels() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/service/levels?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/levels?ordering='+this.sort
                }
                this.listLevels = await fetch(url, {
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
            addSidebox() {
                this.AddClass = 'sidebox-active'
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-deactive'
                this.$refs.addDateCreate.value = new Date().toLocaleDateString('en-CA')
                this.SideBoxChecked = true
            },
            async newLevel() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addLevel.value == '') {
                    showBanner('.banner.error', 'Поле "Наименование темы" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/level_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'level': this.$refs.addLevel.value,
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
                            this.getLevels()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            findSidebox() {
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.AddClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async findLevels() {
                if (this.$refs.findDateCreate.value != '') {
                    this.findString = 'date_create='+this.$refs.findDateCreate.value+'&'
                }
                if (this.$refs.findLevel.value != '') {
                    this.findString = 'level='+this.$refs.findLevel.value+'&'
                }
                this.getLevels()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
            async deleteLevel(level_id) {
            if (confirm('Вы действительно хотите удалить тему вопросов? Все вопросы этой темы будут удалены!')){
                const del = await fetch(this.$store.state.backendUrl+'/api/service/level_delete/'+level_id+'/', {
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
                    this.getLevels();
                }
            }
        },
            async editSideboxLevel(level_id) {
                this.editLevelObj = await fetch(this.$store.state.backendUrl+'/api/service/level/'+level_id+'/', {
                  method: 'get',
                  headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  }
                })
                .then(resp => resp.json())
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-active'
                this.FindClass = 'sidebox-deactive'
                this.AddClass = 'sidebox-deactive'
                this.$refs.editDateCreate.value = new Date(
                     Number(this.editLevelObj['date_create'].substring(6)),
                     Number(this.editLevelObj['date_create'].substring(3,5))-1,
                     Number(this.editLevelObj['date_create'].substring(0,2)),
                ).toLocaleDateString('en-CA')
                this.$refs.editLevel.value = this.editLevelObj['level']
                this.SideBoxChecked = true
            },
            async editLevelFunc() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.editLevel.value == '') {
                    showBanner('.banner.error', 'Поле "Наименование темы" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/level_update/'+this.editLevelObj['id']+'/', {
                      method: 'PATCH',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'level': this.$refs.editLevel.value,
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
                            this.getLevels()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            }
        },
        created() {
            this.getLevels()
        }
    }
</script>

<style>

</style>