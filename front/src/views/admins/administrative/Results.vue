<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif"><br>
            <b style="color: #00415d">{{ info }}</b>
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Результаты олимпиад
             </h3><br>
                <a href="#" @click = "findSidebox();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-magnifying-glass" :style="{ color: white }"/>&nbsp;Поиск
                        </button>
                    </div>
                </a>
            <br><br>
            <div class="container-table">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th>
                                    Тема/дата проведения <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('event_date');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Участники</th>
                                <th>Средний балл</th>
                                <th>Подсчет результатов</th>
                                <th>Выгрузка в Excel</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="olympiad in listOlympiads">
                                <td>
                                    <b>"{{ olympiad.theme }}"</b><br>
                                    ({{ olympiad.event_date }})
                                </td>
                                <td class="no-wrap">
                                    <div v-if="olympiad.total_count !== 0">
                                        <router-link :to="`/admin/results/participants?olympiad_id=`+olympiad.id">
                                            {{ olympiad.complete_count }} из {{ olympiad.total_count }}
                                        </router-link>
                                    </div>
                                    <div v-if="olympiad.total_count === 0">
                                        0
                                    </div>
                                </td>
                                <td class="no-wrap">
                                    {{ olympiad.avg_points }}
                                </td>
                                <td>
                                    <a href="javascript:void(0)">
                                        <div style="display: inline-block;" @click="Recount(olympiad.id);">
                                            <font-awesome-icon icon="fa-solid fa-calculator" size="2x"/>
                                        </div>
                                    </a>
                                </td>
                                <td>
                                    <a href="javascript:void(0)">
                                        <div style="display: inline-block;" @click="DownloadResult(olympiad.id);">
                                            <font-awesome-icon icon="fa-solid fa-file-excel" size="2x"/>
                                        </div>
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
            <p v-bind:class="[FindClass]">Поиск результатов</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Тема олимпиады: </center>
                </td>
                <td >
                    <input type="text" class="form-control text-center" ref="findOlympName">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Дата проведения:</center>
                </td>
                <td>
                    <input type="date" class="form-control text-center" ref="findOlympDate">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Фамилия участника:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="findSurname">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Имя участника:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="findName">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Идентификатор участника:</center>
                </td>
                <td>
                    <input type="text" v-mask="'#####-#####'" class="form-control text-center" ref="findIdentifier">
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
        name: "Results",
        components: {
            Header, AdminMenu, SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                info: '',
                findString: '',
                ButtonClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listOlympiads:[],
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                sort: '-event_date'
            }
        },
        methods: {
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
                    url = this.$store.state.backendUrl+'/api/service/results_olympiads?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/results_olympiads?ordering='+this.sort
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
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            findSidebox(){
                this.findStudyKind = ''
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async findOlympiads(){
                if (this.$refs.findOlympName.value != '') {
                    this.findString = 'theme='+this.$refs.findOlympName.value+'&'
                }
                if (this.$refs.findOlympDate.value != '') {
                    this.findString = 'event_date='+this.$refs.findOlympDate.value+'&'
                }
                if (this.$refs.findSurname.value != '') {
                    this.findString = 'participant_surname='+this.$refs.findSurname.value+'&'
                }
                if (this.$refs.findName.value != '') {
                    this.findString = 'participant_name='+this.$refs.findName.value+'&'
                }
                if (this.$refs.findIdentifier.value != '') {
                    this.findString += 'participant_id='+this.$refs.findIdentifier.value+'&'
                }
                this.getOlympiads()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
            async Recount(olympiad_id) {
                if (confirm('Вы уверены, что хотите перерасчитать результаты?')) {
                    this.info = 'Подождите, идет перерасчет результатов олимпиады...'
                    this.LoadClass = 'vue-active'
                    this.ContentClass = 'vue-deactive'
                    await fetch(this.$store.state.backendUrl+'/api/service/recount_olympiad/'+olympiad_id+'/', {
                      method: 'GET',
                      headers: {
                          'Authorization': 'Token '+localStorage.getItem('access_token'),
                      },
                    })
                    .then(resp => {
                      if (resp.status == 200) {
                          return resp.json().then(data => {
                            showBanner('.banner.success', data.success)
                          })
                      } else {
                         showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                         return false
                      }
                    })
                    this.getOlympiads()
                }
            },
            async DownloadResult(olympiad_id) {
                this.info = 'Подождите, формируем файл результатов для скачивания...'
                this.LoadClass = 'vue-active'
                this.ContentClass = 'vue-deactive'
                await fetch(this.$store.state.backendUrl+'/api/service/results_download/'+olympiad_id+'/', {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                    }
                })
                .then(res => {
                    if (res.status == 400) {
                        showBanner('.banner.error', 'Нет результатов для выбранной олимпиады')
                        return false
                    } else {
                        return res.blob().then(blob => {
                            var file = window.URL.createObjectURL(blob);
                            window.location.assign(file);
                        })
                    }
                })
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            async deleteApp(app_id){
                if (confirm('Вы действительно хотите удалить заявку?')){
                    const del = await fetch(this.$store.state.backendUrl+'/api/users/app_delete/'+app_id+'/', {
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
                        this.getApps();
                    }
                }
            },
        },
        created() {
            this.getOlympiads()
        }
    }
</script>

<style>

</style>