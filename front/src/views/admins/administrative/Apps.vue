<template>
    <Header />
    <AdminMenu />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../../assets/gifs/load.gif">
        </div>
        <div v-bind:class="[ContentClass]">
            <h3 class="table-name" style="color: #00415d;">
                Поданные заявки
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
                                    Дата подачи заявки <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('date_create');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>Пользователь</th>
                                <th>Участник</th>
                                <th>Год обучения/<br>Срок реализации программы</th>
                                <th>
                                    Вид образования <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('study_kind');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>ФИО преподавателя</th>
                                <th>Группа</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="app in listApps">
                                <td class="no-wrap">
                                    {{ app.date_create }}<br>
                                    <a href="#" @click = "deleteApp(app.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </a>&nbsp;&nbsp;&nbsp;
                                    <a href="#" @click = "editSidebox(app.id);" style="color: #00415d;">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    </a>
                                </td>
                                <td>{{ app.profile }}</td>
                                <td class="no-wrap">
                                    {{ app.surname }} {{ app.name }}<br>
                                    Возраст: {{ app.age }}<br>
                                    ID: <b>{{ app.identifier }}</b>
                                </td>
                                <td>{{ app.study_year }}/{{ app.study_duration }}</td>
                                <td>{{ app.study_kind }}</td>
                                <td>{{ app.teacher }}</td>
                                <td class="no-wrap">{{ app.group }}</td>
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
            <p v-bind:class="[AddClass]">Новая заявка</p>
            <p v-bind:class="[UploadClass]">Загрузка заявок</p>
            <p v-bind:class="[EditClass]">Изменение заявки</p>
            <p v-bind:class="[FindClass]">Поиск заявок</p>
        </template>
        <template v-slot:sidebox-text>
        </template>
        <template v-slot:main-table-trs>
            <tr>
                <td>
                    <center>Дата подачи заявки: </center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="date" class="form-control text-center" ref="addDateCreate" disabled>
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="date" class="form-control text-center" ref="editDateCreate" disabled>
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="date" ref="findDateCreate" class="form-control text-center">
                </td>
            </tr>
            <tr v-if="AddClass === 'sidebox-deactive'">
                <td>
                    <center>Пользователь:</center>
                </td>
                <td v-if="EditClass === 'sidebox-active'" v-bind:class="[editClass]">
                    <center><b>{{ editApp.profile }}</b></center>
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findUser">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Фамилия:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="text" class="form-control text-center" ref="addSurname">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editSurname">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findSurname">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Имя:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="text" class="form-control text-center" ref="addName">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editName">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findName">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Возраст:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="number" min="10" class="form-control text-center" ref="addAge">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="number" min="10" class="form-control text-center" ref="editAge">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="number" min="10" class="form-control text-center" ref="findAge">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Год обучения:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="number" min="0" class="form-control text-center" ref="addStudyYear">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="number" min="0" class="form-control text-center" ref="editStudyYear">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="number" min="0" class="form-control text-center" ref="findStudyYear">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Вид образования:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <select class="form-control text-center" v-model="addStudyKind">
                        <option v-for="kind in listStudyKind">
                            {{ kind }}
                        </option>
                    </select>
                </td>
                <td v-bind:class="[EditClass]">
                    <select class="form-control text-center" v-model="editStudyKind">
                        <option v-for="kind in listStudyKind">
                            {{ kind }}
                        </option>
                    </select>
                </td>
                <td v-bind:class="[FindClass]">
                    <select class="form-control text-center" v-model="findStudyKind">
                        <option v-for="kind in listStudyKind">
                            {{ kind }}
                        </option>
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <center>Срок реализации программы обучения:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="number" min="0" class="form-control text-center" ref="addStudyDur">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="number" min="0" class="form-control text-center" ref="editStudyDur">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="number" min="0" class="form-control text-center" ref="findStudyDur">
                </td>
            </tr>
            <tr>
                <td>
                    <center>ФИО преподавателя:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="text" class="form-control text-center" ref="addTeacher">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editTeacher">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findTeacher">
                </td>
            </tr>
            <tr>
                <td>
                    <center>Группа:</center>
                </td>
                <td v-bind:class="[AddClass]">
                    <input type="text" class="form-control text-center" ref="addGroup">
                </td>
                <td v-bind:class="[EditClass]">
                    <input type="text" class="form-control text-center" ref="editGroup">
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" class="form-control text-center" ref="findGroup">
                </td>
            </tr>
            <tr v-if="FindClass === 'sidebox-active'">
                <td>
                    <center>Идентификатор:</center>
                </td>
                <td v-bind:class="[FindClass]">
                    <input type="text" v-mask="'#####-#####'" class="form-control text-center" ref="findId">
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
                        type="button" @click="addApp();">
                        Добавить
                    </button>
                </div>
                <div v-bind:class="[EditClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', EditClass]"
                        type="button" @click="editAppFunc();">
                        Изменить
                    </button>
                </div>
                <div v-bind:class="[FindClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', FindClass]"
                        type="button" @click="findApps();">
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
        name: "AdminApps",
        components: {
            Header, AdminMenu, SideBox
        },
        data() {
            return {
                SideBoxChecked: false,
                findString: '',
                ButtonClass: 'sidebox-deactive',
                AddClass: 'sidebox-deactive',
                EditClass: 'sidebox-deactive',
                FindClass: 'sidebox-deactive',
                ButtonLoadClass: 'sidebox-deactive',
                listStudyKind: ['Общее', 'Профессиональное', 'Дополнительное'],
                listApps:[],
                editApp:[],
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
                this.getApps();
            },
            async getApps() {
                let url = ''
                if (this.findString != ''){
                    url = this.$store.state.backendUrl+'/api/admins/apps?ordering='+this.sort+'&'+this.findString
                } else {
                    url = this.$store.state.backendUrl+'/api/admins/apps?ordering='+this.sort
                }
                this.listApps = await fetch(url, {
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
            addSidebox(){
                this.AddClass = 'sidebox-active'
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-deactive'
                this.UploadClass = 'sidebox-deactive'
                this.$refs.addDateCreate.value = new Date().toLocaleDateString('en-CA')
                this.SideBoxChecked = true
            },
            async addApp(){
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.addSurname.value == '') {
                    showBanner('.banner.error', 'Поле "Фамилия" не может быть пустым')
                } else if (this.$refs.addName.value == '') {
                    showBanner('.banner.error', 'Поле "Имя" не может быть пустым')
                } else if (this.$refs.addAge.value == '') {
                    showBanner('.banner.error', 'Поле "Возраст" не может быть пустым')
                } else if (this.$refs.addStudyYear.value == '') {
                    showBanner('.banner.error', 'Поле "Год обучения" не может быть пустым')
                } else if (this.addStudyKind == null) {
                    showBanner('.banner.error', 'Поле "Вид образования" не может быть пустым')
                } else if (this.$refs.addTeacher.value == '') {
                    showBanner('.banner.error', 'Поле "ФИО преподавателя" не может быть пустым')
                }else if (this.$refs.addStudyDur.value == '') {
                    showBanner('.banner.error', 'Поле "Срок реализации программы обучения" не может быть пустым')
                } else if (this.$refs.addGroup.value == '') {
                    showBanner('.banner.error', 'Поле "Группа" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/users/app_new/', {
                      method: 'POST',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'surname': this.$refs.addSurname.value,
                        'name': this.$refs.addName.value,
                        'age': this.$refs.addAge.value,
                        'study_year': this.$refs.addStudyYear.value,
                        'study_kind': this.addStudyKind,
                        'study_duration': this.$refs.addStudyDur.value,
                        'teacher': this.$refs.addTeacher.value,
                        'group': this.$refs.addGroup.value,
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
                            this.getApps()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            },
            findSidebox(){
                this.AddClass = 'sidebox-deactive'
                this.findStudyKind = ''
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-deactive'
                this.FindClass = 'sidebox-active'
                this.UploadClass = 'sidebox-deactive'
                this.SideBoxChecked = true
            },
            async findApps(){
                if (this.$refs.findDateCreate.value != '') {
                    this.findString = 'data_create='+this.$refs.findDateCreate.value+'&'
                }
                if (this.$refs.findSurname.value != '') {
                    this.findString = 'surname='+this.$refs.findSurname.value+'&'
                }
                if (this.$refs.findUser.value != '') {
                    this.findString = 'user='+this.$refs.findUser.value+'&'
                }
                if (this.$refs.findName.value != '') {
                    this.findString = 'name='+this.$refs.findName.value+'&'
                }
                if (this.$refs.findAge.value != '') {
                    this.findString += 'age='+this.$refs.findAge.value+'&'
                }
                if (this.$refs.findStudyYear.value != '') {
                    this.findString += 'study_year='+this.$refs.findStudyYear.value+'&'
                }
                if (this.findStudyKind != null && this.findStudyKind != '') {
                    this.findString += 'study_kind='+this.findStudyKind+'&'
                }
                if (this.$refs.findTeacher.value != '') {
                    this.findString += 'teacher='+this.$refs.findTeacher.value+'&'
                }
                if (this.$refs.findStudyDur.value != '') {
                    this.findString += 'study_duration='+this.$refs.findStudyDur.value+'&'
                }
                if (this.$refs.findGroup.value != '') {
                    this.findString += 'group='+this.$refs.findGroup.value+'&'
                }
                if (this.$refs.findId.value != '') {
                    this.findString += 'identifier='+this.$refs.findId.value
                }
                this.getApps()
                this.SideBoxChecked = false
                showBanner('.banner.success', 'Поиск завершен');
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
            async editSidebox(id){
                this.editApp = await fetch(this.$store.state.backendUrl+'/api/admins/app/'+id+'/', {
                  method: 'get',
                  headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token'),
                  }
                })
                .then(resp => resp.json())
                this.AddClass = 'sidebox-deactive'
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
                this.EditClass = 'sidebox-active'
                this.FindClass = 'sidebox-deactive'
                this.UploadClass = 'sidebox-deactive'
                this.$refs.editDateCreate.value = new Date(
                     Number(this.editApp['date_create'].substring(6)),
                     Number(this.editApp['date_create'].substring(3,5))-1,
                     Number(this.editApp['date_create'].substring(0,2)),
                ).toLocaleDateString('en-CA')
                this.$refs.editSurname.value = this.editApp['surname']
                this.$refs.editName.value = this.editApp['name']
                this.$refs.editAge.value = this.editApp['age']
                this.$refs.editStudyYear.value = this.editApp['study_year']
                this.editStudyKind = this.editApp['study_kind']
                this.$refs.editTeacher.value = this.editApp['teacher']
                this.$refs.editStudyDur.value = this.editApp['study_duration']
                this.$refs.editGroup.value = this.editApp['group']
                this.SideBoxChecked = true
            },
            async editAppFunc() {
                this.ButtonClass = 'sidebox-deactive'
                this.ButtonLoadClass = 'sidebox-active'
                if (this.$refs.editSurname.value == '') {
                    showBanner('.banner.error', 'Поле "Фамилия" не может быть пустым')
                } else if (this.$refs.editName.value == '') {
                    showBanner('.banner.error', 'Поле "Имя" не может быть пустым')
                } else if (this.$refs.editAge.value == '') {
                    showBanner('.banner.error', 'Поле "Возраст" не может быть пустым')
                } else if (this.$refs.editStudyYear.value == '') {
                    showBanner('.banner.error', 'Поле "Год обучения" не может быть пустым')
                } else if (this.editStudyKind == null) {
                    showBanner('.banner.error', 'Поле "Вид образования" не может быть пустым')
                } else if (this.$refs.editTeacher.value == '') {
                    showBanner('.banner.error', 'Поле "ФИО преподавателя" не может быть пустым')
                }else if (this.$refs.editStudyDur.value == '') {
                    showBanner('.banner.error', 'Поле "Срок реализации программы обучения" не может быть пустым')
                } else if (this.$refs.editGroup.value == '') {
                    showBanner('.banner.error', 'Поле "Группа" не может быть пустым')
                } else {
                    await fetch(this.$store.state.backendUrl+'/api/users/app_edit/'+this.editApp['id']+'/', {
                      method: 'PATCH',
                      headers: {
                        'X-CSRFToken': getCookie("csrftoken"),
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Token '+localStorage.getItem('access_token')
                      },
                      body: JSON.stringify({
                        'surname': this.$refs.editSurname.value,
                        'name': this.$refs.editName.value,
                        'age': this.$refs.editAge.value,
                        'study_year': this.$refs.editStudyYear.value,
                        'study_kind': this.editStudyKind,
                        'study_duration': this.$refs.editStudyDur.value,
                        'teacher': this.$refs.editTeacher.value,
                        'group': this.$refs.editGroup.value
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
                            this.getApps()
                            this.SideBoxChecked = false
                        }
                    })
                }
                this.ButtonClass = 'sidebox-active'
                this.ButtonLoadClass = 'sidebox-deactive'
            }
        },
        created() {
            this.getApps()
        }
    }
</script>

<style>

</style>