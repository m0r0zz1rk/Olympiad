<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                type="button" @click="$router.push('/admin/olympiads')">
                Вернуться к списку олимпиад
            </button>
            <h3 class="table-name" style="color: #00415d;">
                Распределение тем вопросов олимпиады<br>
                "{{ olympiadTheme }}"
            </h3><br>
            <a href="#" @click = "addSidebox();">
                <div style="display: inline;">
                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button">
                        <font-awesome-icon icon="fa-solid fa-plus" :style="{ color: white }"/>&nbsp;Добавить
                    </button>
                </div>
            </a>&nbsp;
            <br><br>
            <div class="container-table">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th>Порядковый номер</th>
                                <th>Тема вопросов</th>
                                <th>Удалить</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="level in listOlympiadLevels">
                                <td class="no-wrap">{{ level.seq_number }}</td>
                                <td class="no-wrap">{{ level.level }} </td>
                                <td class="no-wrap">
                                    <a href="#" @click = "deleteLevel(level.id);" style="color: #00415d;">
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
    <SideBox>
        <template v-slot:side-chb>
            <input type="checkbox" id="side-checkbox" v-model="SideBoxChecked"/>
        </template>
        <template v-slot:sidebox-title>
            <p>Добавление темы</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Порядковый номер: </center>
                </td>
                <td>
                    <input type="number" min="1" class="form-control text-center" ref="addSeqNumber">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Тема вопросов: </center>
                </td>
                <td>
                    <select class="form-control text-center" v-model="addLevel">
                        <option v-for="level in listLevels" :value="level.id">
                            {{ level.level }}
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
                <div>
                    <button class="btn btn-lg btn-primary m-auto iohk-butt sidebox-active"
                        type="button" @click="addLevelFunc();">
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
    import AdminMenu from "../../../components/AdminMenu.vue"

    export default {
        name: "OlympiadLevels",
        components: {
            Header,
            AdminMenu,
            SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                olympiadTheme: '',
                ButtonClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listOlympiadLevels: [],
                listLevels:[],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
            }
        },
        methods: {
            async getOlympiadTheme(){
                let response = await fetch(this.$store.state.backendUrl+'/api/service/olympiad/'+this.$route.query.olympiad_id+'/', {
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
                this.olympiadTheme = response.theme
                return null
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
            async getOlympiadLevels() {
                this.listOlympiadLevels = await fetch(this.$store.state.backendUrl+'/api/service/olympiads_levels?olympiad_id='+this.$route.query.olympiad_id, {
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
            checkSeqNumber() {
                let check = false
                let sqn = this.$refs.addSeqNumber.value
                $.each(this.listOlympiadLevels, function(index, rec){
                    if (rec.seq_number == sqn) {
                        check = true
                        return false
                    }
                })
                return check
            },
            async addLevelFunc() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addSeqNumber.value == '') {
                    showBanner('.banner.error', 'Поле "Порядковый номер" не может быть пустым')
                    this.ButtonClass = 'sidebox-active'
                    this.ButtonLoadClass = 'sidebox-deactive'
                    return false
                } else if (this.addLevel == null) {
                    showBanner('.banner.error', 'Поле "Тема вопросов" не может быть пустым')
                    this.ButtonClass = 'sidebox-active'
                    this.ButtonLoadClass = 'sidebox-deactive'
                    return false
                } else if (this.checkSeqNumber()) {
                    showBanner('.banner.error', 'Указанный порядковый номер уже используется для этой олимпиады')
                    this.ButtonClass = 'sidebox-active'
                    this.ButtonLoadClass = 'sidebox-deactive'
                    return false
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/service/olympiad_level_add/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'olympiad': this.$route.query.olympiad_id,
                        'seq_number': this.$refs.addSeqNumber.value,
                        'level': this.addLevel
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
                            this.getOlympiadLevels()
                            this.SideBoxChecked = false
                        }
                    })
                }
            },
            async deleteLevel(level_id) {
                if (confirm('Вы действительно хотите Тема вопроса из олимпиады?')) {
                    await fetch(this.$store.state.backendUrl+'/api/service/olympiad_level_delete/'+level_id+'/', {
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
                            this.getOlympiadLevels()
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
            this.getOlympiadTheme()
            this.getOlympiadLevels()
            this.getLevels()
        }
    }
</script>

<style>
</style>