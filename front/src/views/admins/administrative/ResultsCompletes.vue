<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif"><br>
        </div>
        <div v-bind:class="[ContentClass]">
            <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                type="button" @click="$router.push('/admin/results')">
                Вернуться к списку результатов
            </button>
            <h3 class="table-name" style="color: #00415d;">
                Список участников олимпиады<br>"<b>{{ olympicTheme }}</b>"
            </h3>
                <a href="#" @click = "findSidebox();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-magnifying-glass" :style="{ color: white }"/>&nbsp;Поиск
                        </button>
                    </div>
                </a>
            <br>
            <div class="container-table">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th>Образовательная организация</th>
                                <th>
                                    Участник <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('surname');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Статус</th>
                                <th>Баллы</th>
                                <th>Просмотр ответов</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="participant in listParticipants">
                                <td>
                                    {{ participant.oo }}
                                </td>
                                <td>
                                    <b>{{ participant.surname }} {{ participant.name }}</b><br>
                                    {{ participant.group }}<br>
                                    <b>{{ participant.identifier }}</b>
                                </td>
                                <td class="no-wrap">
                                    <b v-if="participant.is_complete === 'Не проходил'"
                                        style="color: red;">
                                        {{ participant.is_complete }}
                                    </b>
                                    <b v-if="participant.is_complete === 'В процессе'"
                                        style="color: yellow;">
                                        {{ participant.is_complete }}
                                    </b>
                                    <b v-if="participant.is_complete === 'Завершил прохождение'"
                                        style="color: green;">
                                        {{ participant.is_complete }}
                                    </b>
                                </td>
                                <td>
                                    <div v-if="participant.have_results">
                                        <b>{{ participant.points }}</b>
                                    </div>
                                </td>
                                <td>
                                    <div v-if="participant.is_complete === 'Завершил прохождение'">
                                        <div v-if="participant.have_results">
                                            <router-link
                                            :to="`/admin/result_detail?olympiad_id=`+$route.query.olympiad_id+`&identifier=`+participant.identifier">
                                                <div style="display: inline-block;" @click="sorted('event_date');">
                                                    <font-awesome-icon icon="fa-solid fa-table-list" size="2x"/>
                                                </div>
                                            </router-link>
                                        </div>
                                        <div v-if="!(participant.have_results)">
                                            <b>Выполните<br>подсчет<br>результатов</b>
                                        </div>
                                    </div>
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
            <p v-bind:class="[FindClass]">Поиск участников</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Фамилия: </center>
                </td>
                <td >
                    <input type="text" class="form-control text-center" ref="findSurname">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Имя:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="findName">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Название образовательной организации:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center" ref="findOo">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Идентификатор:</center>
                </td>
                <td>
                    <input type="text" v-mask="'#####-#####'" class="form-control text-center" ref="findId">
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
                        type="button" @click="findParticipants();">
                        Поиск
                    </button>
                </div>
            </div>
        </template>
    </SideBox>
</template>

<script>
    import Header from "../../../components/Header.vue"
    import AdminMenu from "../../../components/AdminMenu.vue"
    import SideBox from "../../../components/SideBox.vue"

    export default {
        name: "ResultsCompletes",
        components: {
            Header, AdminMenu, SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                olympicTheme: '',
                ButtonClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listParticipants:[],
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
                this.getParticipants();
            },
            async getTheme() {
                let url = this.$store.state.backendUrl+'/api/service/olympiad_theme?olympiad_id='+this.$route.query.olympiad_id
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
                this.olympicTheme = response.success
            },
            async getParticipants() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/service/results_completes?olympiad_id='+
                            this.$route.query.olympiad_id+'&ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/service/results_completes?olympiad_id='+
                        this.$route.query.olympiad_id+'&ordering='+this.sort
                }
                this.listParticipants = await fetch(url, {
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
            async findParticipants(){
                this.findString = ''
                if (this.$refs.findSurname.value != '') {
                    this.findString = 'surname='+this.$refs.findSurname.value+'&'
                }
                if (this.$refs.findName.value != '') {
                    this.findString = 'name='+this.$refs.findName.value+'&'
                }
                if (this.$refs.findOo.value != '') {
                    this.findString = 'oo='+this.$refs.findOo.value+'&'
                }
                if (this.$refs.findId.value != '') {
                    this.findString = 'identifier='+this.$refs.findId.value+'&'
                }
                this.getParticipants()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
        },
        created() {
            this.getTheme()
            this.getParticipants()
        }
    }
</script>

<style>

</style>