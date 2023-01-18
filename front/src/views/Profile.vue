<template>
    <Header/>
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <div class="container-table">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th colspan="2">
                                    <h4 class="center-text">Информация о пользователе</h4>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Фамилия</td>
                                <td>
                                    {{ profileInfo.surname }}
                                </td>
                            </tr>
                            <tr>
                                <td>Имя</td>
                                <td>
                                    {{ profileInfo.name }}
                                </td>
                            </tr>
                            <tr>
                                <td>Отчество</td>
                                <td>
                                    {{ profileInfo.patronymic }}
                                </td>
                            </tr>
                            <tr>
                                <td>Полное наименование ОО</td>
                                <td>
                                    {{ profileInfo.oo_fullname }}
                                </td>
                            </tr>
                            <tr>
                                <td>Физический адрес ОО</td>
                                <td>
                                    {{ profileInfo.oo_address }}
                                </td>
                            </tr>
                            <tr>
                                <td>Должность</td>
                                <td>
                                    {{ profileInfo.position }}
                                </td>
                            </tr>
                            <tr>
                                <td>Номер телефона</td>
                                <td>
                                    {{ profileInfo.phone }}
                                </td>
                            </tr>
                            <tr>
                                <td>Email</td>
                                <td>
                                    {{ profileInfo.email }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <a href="#" @click = "editInfo();">
                <div style="display: inline;">
                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button">
                        Изменить данные
                    </button>
                </div>
            </a>&nbsp;
            <a href="#" @click = "editPass();">
                <div style="display: inline;">
                    <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                        type="button">
                        Смена пароля
                    </button>
                </div>
            </a>
        </div>
    </div>
    <SideBox>
        <template v-slot:side-chb>
            <input type="checkbox" id="side-checkbox" v-model="SideBoxChecked"/>
        </template>
        <template v-slot:sidebox-title>
            <p v-bind:class="[EditInfoClass]">Редактирование информации</p>
            <p v-bind:class="[EditPasswordClass]">Смена пароля</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Фамилия:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center"
                        :value="profileInfo.surname" ref="editSurname">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Имя:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center"
                        :value="profileInfo.name" ref="editName">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Отчество:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center"
                        :value="profileInfo.patronymic"  ref="editPatronymic">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Наименование ОО:</center>
                </td>
                <td>
                    <textarea class="form-control"
                        :value="profileInfo.oo_fullname" ref="editOo"></textarea>
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Адрес ОО:</center>
                </td>
                <td>
                    <textarea class="form-control"
                        :value="profileInfo.oo_address" ref="editOoAddress"></textarea>
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Должность:</center>
                </td>
                <td>
                    <input type="text" class="form-control text-center"
                        :value="profileInfo.position" ref="editPosition">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Контактный телефон:</center>
                </td>
                <td>
                    <input type="text" v-mask="'+7 (###) ###-##-##'" class="form-control text-center"
                        :value="profileInfo.phone" ref="editPhone">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-deactive'">
                <td>
                    <center>Email:</center>
                </td>
                <td>
                    <input type="email" class="form-control text-center"
                        :value="profileInfo.email" ref="editEmail">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-active'">
                <td>
                    <center>Пароль:</center>
                </td>
                <td>
                    <input type="password" class="form-control text-center" ref="passw">
                </td>
            </tr>
            <tr v-if="EditPasswordClass === 'sidebox-active'">
                <td>
                    <center>Подтверждение:</center>
                </td>
                <td>
                    <input type="password" class="form-control text-center" ref="passw2">
                </td>
            </tr>
        </template>
        <template v-slot:sidebox-button>
            <div v-bind:class="[ButtonLoadClass]">
                <img src="../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[EditInfoClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditInfoClass]"
                        type="button" @click="editInfoFunc();">
                        Изменить
                    </button>
                </div>
                <div v-bind:class="[EditPasswordClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditPasswordClass]"
                        type="button" @click="ChangePassw();">
                        Сменить
                    </button>
                </div>
            </div>
        </template>
    </SideBox>
</template>

<script>
    import Header from "../components/Header.vue"
    import SideBox from "../components/SideBox.vue"

    export default {
        name: 'Profile',
        components: {
            Header,
            SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                profileInfo: [],
                EditInfoClass: 'sidebox-deactive',
                EditPasswordClass: 'sidebox-deactive',
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive'
            }
        },
        methods: {
            async getInfo(){
                await fetch(this.$store.state.backendUrl+'/api/authen/profile', {
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
                .then(data => {
                    this.profileInfo = data.profile
                })
                this.LoadClass = 'vue-deactive'
                this.ContentClass = 'vue-active'
            },
            editInfo() {
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditInfoClass = 'sidebox-active'
                this.EditPasswordClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async editInfoFunc() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.editSurname.value == '') {
                    showBanner('.banner.error', 'Поле "Фамилия" не может быть пустым')
                } else if (this.$refs.editName.value == '') {
                    showBanner('.banner.error', 'Поле "Имя" не может быть пустым')
                } else if (this.$refs.editPatronymic.value == '') {
                    showBanner('.banner.error', 'Поле "Отчество" не может быть пустым')
                } else if (this.$refs.editOo.value == '') {
                    showBanner('.banner.error', 'Поле "Наименование ОО" не может быть пустым')
                } else if (this.$refs.editOoAddress.value == '') {
                    showBanner('.banner.error', 'Поле "Адрес ОО" не может быть пустым')
                } else if (this.$refs.editPosition.value == '') {
                    showBanner('.banner.error', 'Поле "Должность" не может быть пустым')
                } else if (this.$refs.editPhone.value == '') {
                    showBanner('.banner.error', 'Поле "Телефон" не может быть пустым')
                } else if (this.$refs.editEmail.value == '') {
                    showBanner('.banner.error', 'Поле "Email" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/authen/profile_update/', {
                      method: 'PATCH',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'role': this.editRole,
                        'surname': this.$refs.editSurname.value,
                        'name': this.$refs.editName.value,
                        'patronymic': this.$refs.editPatronymic.value,
                        'oo_fullname': this.$refs.editOo.value,
                        'oo_address': this.$refs.editOoAddress.value,
                        'position': this.$refs.editPosition.value,
                        'phone': this.$refs.editPhone.value,
                        'email': this.$refs.editEmail.value
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
                            this.getInfo()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            editPass() {
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditInfoClass = 'sidebox-deactive'
                this.EditPasswordClass = 'sidebox-active'
                this.SideBoxChecked = true
            },
            async ChangePassw() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.passw.value == '') {
                    showBanner('.banner.error', 'Поле "Пароль" не может быть пустым')
                } else if (this.$refs.passw2.value == '') {
                    showBanner('.banner.error', 'Поле "Подтверждение" не может быть пустым')
                } else if (this.$refs.passw.value != this.$refs.passw2.value) {
                    showBanner('.banner.error', 'Пароли должны совпадать')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/authen/password_update/', {
                      method: 'PATCH',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'passw': this.$refs.passw.value,
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
                            this.getInfo()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            }
        },
        created(){
            this.getInfo()
        }
    }
</script>

<style>
 .center-text{
    margin: 0 auto;
 }
</style>