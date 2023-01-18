<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Зарегистрированные пользователи
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
            <div class="container-table" style="width: 95vw;">
                <div class="table-wrapper">
                    <table class="fl-table">
                        <thead>
                            <tr>
                                <th>
                                    Роль
                                </th>
                                <th>
                                    Фамилия <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('date_create');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Имя <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('surname');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Отчество <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('patronymic');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Образовательная организация
                                </th>
                                <th>
                                    Должность <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('position');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Контактный телефон <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('phone');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in listUsers">
                                <td class="no-wrap">
                                    {{ user.role }}<br>
                                    <a href="#" @click = "deleteUser(user.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a href="#" @click = "editSideboxUser(user.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a href="#" @click = "passwSidebox(user.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-lock" />
                                    </a>
                                </td>
                                <td>{{ user.surname }}</td>
                                <td>{{ user.name }}</td>
                                <td>{{ user.patronymic }}</td>
                                <td>{{ user.oo_fullname }}<br> ({{ user.oo_address }})</td>
                                <td>{{ user.position }}</td>
                                <td class="no-wrap">{{ user.phone }}</td>
                                <td class="no-wrap">{{ user.email }}</td>
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
            <p v-bind:class="[FindClass]">Поиск пользователя</p>
            <p v-bind:class="[EditClass]">Редактирование данных пользователя</p>
            <p v-bind:class="[PasswClass]">Смена пароля</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr v-if="EditClass === 'sidebox-active'">
                <td>
                    <center>Роль:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <select class="form-control text-center mx-auto" v-model="editRole">
                        <option>Администратор</option>
                        <option>Пользователь</option>
                    </select>
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Фамилия:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editSurname">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findSurname">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Имя:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editName">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findName">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Отчество:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editPatronymic">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findPatronymic">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Наименование ОО:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <textarea class="form-control" ref="editOo"></textarea>
                </td>
                <td v-bind:class="[FindClass]">
                    <textarea class="form-control" ref="findOo"></textarea>
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Адрес ОО:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <textarea class="form-control" ref="editOoAddress"></textarea>
                </td>
                <td v-bind:class="[FindClass]">
                    <textarea class="form-control" ref="findOoAddress"></textarea>
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Должность:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editPosition">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findPosition">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Контактный телефон:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" v-mask="'+7 (###) ###-##-##'" class="form-control text-center"
                        ref="editPhone">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" v-mask="'+7 (###) ###-##-##'" class="form-control text-center"
                        ref="findPhone">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-deactive'">
                <td>
                    <center>Email:</center>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="email" class="form-control text-center" ref="editEmail">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="email" class="form-control text-center" ref="findEmail">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-active'">
                <td>
                    <center>Пользователь:</center>
                </td>
                <td>
                    <center>{{ editPasswUser }}</center>
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-active'">
                <td>
                    <center>Пароль:</center>
                </td>
                <td>
                    <input type="password" class="form-control text-center" ref="passw">
                </td>
            </tr>
            <tr v-if="PasswClass === 'sidebox-active'">
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
                <img src="../../../assets/gifs/load.gif" style="margin-left: 50%;">
            </div>
            <div v-bind:class="[ButtonClass]">
                <div v-bind:class="[EditClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditClass]"
                        type="button" @click="editUserFunc();">
                        Изменить
                    </button>
                </div>
                <div v-bind:class="[FindClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                        type="button" @click="findUsers();">
                        Поиск
                    </button>
                </div>
                <div v-bind:class="[PasswClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', PasswClass]"
                        type="button" @click="ChangePassw();">
                        Сменить
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
        name: "Users",
        components: {
            Header, AdminMenu, SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                ButtonClass: 'sidebox-deactive',
                EditClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                PasswClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listUsers:[],
                editUser:[],
                passwUser: [],
                editPasswUser: '',
                LoadClass: 'vue-active',
                ContentClass: 'vue-deactive',
                sort: '-surname'
            }
        },
        methods: {
            sorted(obj) {
                if (this.sort == obj) {
                    this.sort = "-"+obj
                } else {
                    this.sort = obj
                }
                this.getUsers();
            },
            async getUsers() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/admins/users?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/admins/users?ordering='+this.sort
                }
                this.listUsers = await fetch(url, {
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
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.PasswClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async findUsers() {
                if (this.$refs.findSurname.value != '') {
                    this.findString = 'surname='+this.$refs.findSurname.value+'&'
                }
                if (this.$refs.findName.value != '') {
                    this.findString = 'name='+this.$refs.findName.value+'&'
                }
                if (this.$refs.findPatronymic.value != '') {
                    this.findString += 'patronymic='+this.$refs.findPatronymic.value+'&'
                }
                if (this.$refs.findOo.value != '') {
                    this.findString += 'oo_fullname='+this.$refs.findOo.value+'&'
                }
                if (this.$refs.findOoAddress.value != '') {
                    this.findString += 'oo_address='+this.$refs.findOoAddress.value+'&'
                }
                if (this.$refs.findPosition.value != '') {
                    this.findString += 'position='+this.$refs.findPosition.value+'&'
                }
                if (this.$refs.findPhone.value != '') {
                    this.findString += 'phone='+this.$refs.findPhone.value+'&'
                }
                this.getUsers()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
            },
            async deleteUser(user_id) {
            if (confirm('Вы действительно хотите удалить пользователя? Все заявки пользователя также будут удалены!')){
                const del = await fetch(this.$store.state.backendUrl+'/api/admins/user_delete/'+user_id+'/', {
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
                    this.getUsers();
                }
            }
        },
            async editSideboxUser(user_id) {
                this.editUser = await fetch(this.$store.state.backendUrl+'/api/admins/user/'+user_id+'/', {
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
                this.PasswClass = 'sidebox-deactive'
                this.editRole = this.editUser['role']
                this.$refs.editSurname.value = this.editUser['surname']
                this.$refs.editName.value = this.editUser['name']
                this.$refs.editPatronymic.value = this.editUser['patronymic']
                this.$refs.editOo.value = this.editUser['oo_fullname']
                this.$refs.editOoAddress.value = this.editUser['oo_address']
                this.$refs.editPosition.value = this.editUser['position']
                this.$refs.editPhone.value = this.editUser['phone']
                this.$refs.editEmail.value = this.editUser['email']
                this.SideBoxChecked = true
            },
            async editUserFunc() {
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
                    await fetch(this.$store.state.backendUrl+'/api/admins/user_update/'+this.editUser['id']+'/', {
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
                            this.getUsers()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            async passwSidebox(user_id) {
                this.passwUser = await fetch(this.$store.state.backendUrl+'/api/admins/user/'+user_id+'/', {
                  method: 'get',
                  headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  }
                })
                .then(resp => resp.json())
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-deactive'
                this.PasswClass = 'sidebox-active'
                this.editPasswUser = this.passwUser['surname']+' '+this.passwUser['name']+' '+this.passwUser['patronymic']
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
                    await fetch(this.$store.state.backendUrl+'/api/admins/user_changepass/'+this.passwUser['id']+'/', {
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
                            this.getUsers()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            }
        },
        created() {
            this.getUsers()
        }
    }
</script>

<style>

</style>