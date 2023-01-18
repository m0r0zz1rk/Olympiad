<template>
    <ParticipantHeader />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../assets/gifs/load.gif">
            <br><b style="color: #00415d;">{{ info }}</b>
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Добро пожаловать!
            </h3><br>
            <b style="color: #00415d;">Перед началом прохождения олимпиады убедитесь, что информация об участнике, которая отображена в таблице ниже,
            действительна и не содержит ошибок. <br>После проверки приступайте к выполнению олимпиады, нажав на кнопку
            "Начать"</b><br>
            <div class="container-table" style="width: 75%; margin: 0 auto;">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th colspan="2">
                                    Информация об участнике
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Фамилия:</td>
                                <td>{{ participant.surname }}</td>
                            </tr>
                            <tr>
                                <td>Имя:</td>
                                <td>{{ participant.name }}</td>
                            </tr>
                            <tr>
                                <td>Возраст (полных лет):</td>
                                <td>{{ participant.age }}</td>
                            </tr>
                            <tr>
                                <td>Группа/Класс:</td>
                                <td>{{ participant.group }}</td>
                            </tr>
                            <tr>
                                <td>ФИО преподавателя</td>
                                <td>{{ participant.teacher }}</td>
                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>
            <div class="container-table" style="width: 75%; margin: 0 auto;">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th colspan="2">
                                    Информация об олимпиаде
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Тема олимпиады:</td>
                                <td>{{ olympiad.theme }}</td>
                            </tr>
                            <tr>
                                <td>Дата проведения олимпиады:</td>
                                <td>{{ olympiad.event_date }}</td>
                            </tr>
                            <tr>
                                <td>Время на прохождение олимпиады:</td>
                                <td>{{ olympiad.time_complete }} мин.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <button class="btn btn-lg btn-primary m-auto iohk-butt"
                type="button" @click="startOlymp();">
                Начать
            </button>
        </div>
    </div>
</template>

<script>
    import ParticipantHeader from "../../components/ParticipantHeader.vue"

    export default {
        name: "StartPage",
        components: {ParticipantHeader},
        data() {
            return {
                participant: [],
                olympiad: [],
                info: '',
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
            }
        },
        methods: {
            async getParticipantInfo() {
                this.participant = await fetch(this.$store.state.backendUrl+'/api/participants/participant_info/', {
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
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            async getOlympiadInfo() {
                this.olympiad = await fetch(this.$store.state.backendUrl+'/api/participants/olympiad_info/', {
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
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            async startOlymp() {
                this.info = 'Формируем список вопросов...'
                this.LoadClass = 'vue-active'
                this.ContentClass = 'vue-deactive'
                await fetch(this.$store.state.backendUrl+'/api/participants/olympiad_start/', {
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
                      this.$store.dispatch('START_OLYMP_REQUEST')
                        .then(() => {
                          this.$router.push('/olympic')
                        })
                  } else {
                     showBanner('.banner.error', 'Произошла ошибка, повторите попытку позже')
                     this.LoadClass = 'vue-deactive'
                     this.ContentClass = 'vue-active'
                     return false
                  }
                })
            }
        },
        created() {
            this.getParticipantInfo()
            this.getOlympiadInfo()
        }
    }
</script>

<style>
</style>