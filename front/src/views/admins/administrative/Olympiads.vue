<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Олимпиады
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
                                    Дата проведения <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('event_date');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Тема</th>
                                <th>
                                    Сроки подачи заявок <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('date_reg_start');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Время прохождения олимпиады<br>(в минутах)</th>
                                <th>Темы вопросов</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="olympiad in listOlympiads">
                                <td class="no-wrap">
                                    {{ olympiad.event_date }}
                                </td>
                                <td>{{ olympiad.theme }} </td>
                                <td class="no-wrap">
                                    {{ olympiad.date_reg_start }} - {{ olympiad.date_reg_end }}
                                </td>
                                <td>{{ olympiad.time_complete }}</td>
                                <td>
                                    <router-link :to="`/admin/olympiad_levels?olympiad_id=`+olympiad.id" @click = "OlympiadLevels(olympiad.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-layer-group" />
                                    </router-link>
                                </td>
                                <td class="no-wrap">
                                    <a href="#" @click = "deleteOlympiad(olympiad.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a href="#" @click = "editSidebox(olympiad.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    </a>
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
            <p v-bind:class="[FindClass]">Поиск олимпиад</p>
            <p v-bind:class="[EditClass]">Редактирование олимпиады</p>
            <p v-bind:class="[AddClass]">Добавление олимпиады</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Дата проведения: </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="date" class="form-control text-center" ref="addDateEvent">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="date" class="form-control text-center" ref="editDateEvent">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="date" class="form-control text-center" ref="findDateEvent">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Тема: </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <textarea class="form-control" ref="addTheme"></textarea>
                </td>
                <td v-bind:class="[EditClass]">
                    <textarea class="form-control" ref="editTheme"></textarea>
                </td>
                <td v-bind:class="[FindClass]">
                    <textarea class="form-control" ref="findTheme"></textarea>
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-deactive'">
                <td>
                    <center>Дата начала подачи заявок: </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="date" class="form-control text-center" ref="addDateRegStart">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="date" class="form-control text-center" ref="editDateRegStart">
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-deactive'">
                <td>
                    <center>Дата окончания подачи заявок: </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="date" class="form-control text-center" ref="addDateRegEnd">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="date" class="form-control text-center" ref="editDateRegEnd">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Время прохождения олимпиады (в минутах): </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="number" min="10" class="form-control text-center" ref="addTimeComplete">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="number" min="10" class="form-control text-center" ref="editTimeComplete">
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Дата подачи заявок: </center>
                </td>
                <td>
                    <input type="date" class="form-control text-center" ref="findDateReg">
                </td>
            </tr>
        </template>
        <template v-slot:sidebox-button>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../../../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[AddClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', AddClass]"
                        type="button" @click="addOlympiad();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[EditClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditClass]"
                        type="button" @click="editOlympiadFunc();">
                        Изменить
                    </button>
                </div>
                <div v-bind:class="[FindClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                        type="button" @click="findOlympiads();">
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
    import AdminMenu from "../../../components/AdminMenu.vue"

    export default {
        name: "Olympiads",
        components: {
            Header,
            AdminMenu,
            SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                ButtonClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                EditClass: 'sidebox-deactive',
                AddClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listOlympiads:[],
                listOlympiadsLevels: {},
                listQuestionLevels:[],
                editOlympiad: [],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                sort: '-date_event'
            }
        },
        methods: {
            format(inputDate) {
              let day, month, year;

              day = inputDate.substring(8,10)
              month = inputDate.substring(5, 7)
              year = inputDate.substring(0, 4)

              return `${day}.${month}.${year}`;
            },
            sorted(obj) {
                if (this.sort == obj) {
                    this.sort = "-"+obj
                } else {
                    this.sort = obj
                }
                this.getOlympiads();
            },
            async getOlympiads() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/service/olympiads?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/olympiads?ordering='+this.sort
                }
                this.listOlympiads = await fetch(url, {
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
            async getLevels() {
                this.listQuestionLevels = await fetch(this.$store.state.backendUrl+'/api/service/levels', {
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
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.AddClass = 'sidebox-active'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async addOlympiad() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addDateEvent.value == '') {
                    showBanner('.banner.error', 'Поле "Дата проведения" не может быть пустым')
                } else if (this.$refs.addTheme.value == '') {
                    showBanner('.banner.error', 'Поле "Тема" не может быть пустым')
                } else if (this.$refs.addDateRegStart.value == '') {
                    showBanner('.banner.error', 'Поле "Дата начача подачи заявок" не может быть пустым')
                } else if (this.$refs.addDateRegEnd.value == '') {
                    showBanner('.banner.error', 'Поле "Дата окончания подачи заявок" не может быть пустым')
                } else if (this.$refs.addDateRegStart.value > this.$refs.addDateRegEnd.value) {
                    showBanner('.banner.error', 'Некорректо указаны сроки подачи заявок')
                } else if (this.$refs.addTimeComplete.value == '') {
                    showBanner('.banner.error', 'Поле "Время прохождения олимпиады" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/olympiad_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'event_date': this.format(this.$refs.addDateEvent.value),
                        'theme': this.$refs.addTheme.value,
                        'date_reg_start': this.format(this.$refs.addDateRegStart.value),
                        'date_reg_end': this.format(this.$refs.addDateRegEnd.value),
                        'time_complete': this.$refs.addTimeComplete.value,
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
                            this.getOlympiads()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async editSidebox(olympiad_id) {
                this.editOlympiad = await fetch(this.$store.state.backendUrl+'/api/service/olympiad/'+olympiad_id+'/', {
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
                this.$refs.editDateEvent.value = new Date(
                     Number(this.editOlympiad['event_date'].substring(6)),
                     Number(this.editOlympiad['event_date'].substring(3,5))-1,
                     Number(this.editOlympiad['event_date'].substring(0,2)),
                ).toLocaleDateString('en-CA')
                this.$refs.editTheme.value = this.editOlympiad['theme']
                this.$refs.editDateRegStart.value = new Date(
                     Number(this.editOlympiad['date_reg_start'].substring(6)),
                     Number(this.editOlympiad['date_reg_start'].substring(3,5))-1,
                     Number(this.editOlympiad['date_reg_start'].substring(0,2)),
                ).toLocaleDateString('en-CA')
                this.$refs.editDateRegEnd.value = new Date(
                     Number(this.editOlympiad['date_reg_end'].substring(6)),
                     Number(this.editOlympiad['date_reg_end'].substring(3,5))-1,
                     Number(this.editOlympiad['date_reg_end'].substring(0,2)),
                ).toLocaleDateString('en-CA')
                this.$refs.editTimeComplete.value = this.editOlympiad['time_complete']
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.AddClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-active'
                this.FindClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async editOlympiadFunc() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.editDateEvent.value == '') {
                    showBanner('.banner.error', 'Поле "Дата проведения" не может быть пустым')
                } else if (this.$refs.editTheme.value == '') {
                    showBanner('.banner.error', 'Поле "Тема" не может быть пустым')
                } else if (this.$refs.editDateRegStart.value == '') {
                    showBanner('.banner.error', 'Поле "Дата начача подачи заявок" не может быть пустым')
                } else if (this.$refs.editDateRegEnd.value == '') {
                    showBanner('.banner.error', 'Поле "Дата окончания подачи заявок" не может быть пустым')
                } else if (this.$refs.editDateRegStart.value > this.$refs.editDateRegEnd.value) {
                    showBanner('.banner.error', 'Некорректо указаны сроки подачи заявок')
                } else if (this.$refs.editTimeComplete.value == '') {
                    showBanner('.banner.error', 'Поле "Время прохождения олимпиады" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/olympiad_update/'+this.editOlympiad['id']+'/', {
                      method: 'PUT',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'event_date': this.format(this.$refs.editDateEvent.value),
                        'theme': this.$refs.editTheme.value,
                        'date_reg_start': this.format(this.$refs.editDateRegStart.value),
                        'date_reg_end': this.format(this.$refs.editDateRegEnd.value),
                        'time_complete': this.$refs.editTimeComplete.value
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
                            this.getOlympiads()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async deleteOlympiad(olympiad_id) {
                if (confirm('Вы действительно хотите удалить олимпиаду?')) {
                    await fetch(this.$store.state.backendUrl+'/api/service/olympiad_delete/'+olympiad_id+'/', {
                      method: 'DELETE',
                      headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      }
                    })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data.error) {
                            showBanner('.banner.error', data.error)
                            return false
                        } else {
                            showBanner('.banner.success', data.success)
                            this.getOlympiads()
                        }
                    })
                }
            },
            findSidebox() {
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.AddClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async findOlympiads() {
                if (this.$refs.findDateEvent.value != '') {
                    this.findString = 'event_date='+this.$refs.findDateEvent.value+'&'
                }
                if (this.$refs.findTheme.value != '') {
                    this.findString = 'theme='+this.$refs.findTheme.value+'&'
                }
                if (this.$refs.findDateReg.value != '') {
                    this.findString = 'date_reg='+this.$refs.findDateReg.value
                }
                this.getOlympiads()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
            async deleteOlympiad(olympiad_id) {
                if (confirm('Вы действительно хотите удалить олимпиаду?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/service/olympiad_delete/'+olympiad_id+'/', {
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
                        this.getOlympiads();

                    }
                }
            }
        },
        created() {
            this.getOlympiads()
            this.getLevels()
        }
    }
</script>

<style>
</style>