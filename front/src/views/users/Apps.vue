<template>
    <Header />
    <div id="main-content">
        <div v-bind:class="[LoadClass]">
            <img src="../../assets/gifs/load.gif">
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
                <a href="#" @click = "uploadSidebox();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-upload" :style="{ color: white }"/>&nbsp;Загрузить
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
                </a>&nbsp;
                <a href="#" @click = "downloadApps();">
                    <div style="display: inline;">
                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                            type="button">
                            <font-awesome-icon icon="fa-solid fa-download" :style="{ color: white }"/>&nbsp;Выгрузить
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
                                    Дата подачи<br>заявки <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('date_create');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Фамилия <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('surname');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Имя <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('name');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Возраст<br>участника
                                </th>
                                <th>
                                    Год<br>обучения <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('study_year');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Вид образования <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('study_kind');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Срок реализации<br>программы обучения <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('study_duration');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    ФИО преподавателя
                                </th>
                                <th>
                                    Группа <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('group');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
                                <th>
                                    Идентификатор <a href="javascript:void(0)">
                                    <div style="display: inline-block;" @click="sorted('identifier');">
                                        <font-awesome-icon icon="fa-solid fa-sort" :style="{ color: 'white' }"/>
                                    </div></a>
                                </th>
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
                                <td>{{ app.surname }}</td>
                                <td>{{ app.name }}</td>
                                <td>{{ app.age }}</td>
                                <td>{{ app.study_year }}</td>
                                <td>{{ app.study_kind }}</td>
                                <td>{{ app.study_duration }}</td>
                                <td>{{ app.teacher }}</td>
                                <td class="no-wrap">{{ app.group }}</td>
                                <td class="no-wrap">{{ app.identifier }}</td>
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
            <p v-bind:class="[FindClass]">Поиск заявки</p>
        </template>
        <template v-slot:sidebox-text>
            <div v-if="UploadClass === 'sidebox-active'">
                <b>Для успешной загрузки заявок из файла необходимо выполнение следующих условий:</b><br>
                - Формат файла: <b>xlsx</b>(только один лист в файле);<br>
                - Файл должен содержать следующие столбцы (<b>все названия должны совпадать со значением в кавычках и
                 находится на первой строке листа!</b>):<br>
                1. <b>"Фамилия"</b> (текстовый формат)<br>
                2. <b>"Имя"</b> (текстовый формат)<br>
                3. <b>"Возраст"</b> (целое число, количество полных лет)<br>
                4. <b>"Год обучения"</b> (целое число)<br>
                5. <b>"Вид образования"</b> (<i>Общее</i>, <i>Дополнительное</i> или <i>Профессиональное</i>)<br>
                6. <b>"Срок реализации программы обучения"</b> (целое число, лет)<br>
                7. <b>"ФИО преподавателя"</b> (текстовый формат: Иванов Иван Иванович)<br>
                8. <b>"Группа"</b> (текстовый формат, шифр группы/класс: ПрИ.18-2, 10А)<br><br>
                <input type="file" class="form-control m-auto text-center"
                    accept=".xlsx" ref="uploadFile">
            </div>
        </template>
        <template v-slot:main-table-trs>
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
            <tr v-if="UploadClass === 'sidebox-deactive'">
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
                <img src="../../assets/gifs/load.gif" style="margin-left: 50%;">
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
                <div v-bind:class="[UploadClass]">
                    <button v-bind:class="['btn', 'btn-lg', 'btn-primary', 'm-auto', 'iohk-butt', UploadClass]"
                        type="button" @click="uploadApps();">
                        Загрузить
                    </button>
                </div>
            </div>
        </template>
    </SideBox>
</template>

<script>
 import Header from "../../components/Header.vue"
 import SideBox from "../../components/SideBox.vue"

 export default {
    name: "Apps",
    components: {
        Header, SideBox
    },
    data() {
        return {
            SideBoxChecked: false,
            findString: '',
            AddClass: 'sidebox-deactive',
            ButtonClass: 'sidebox-deactive',
            EditClass: 'sidebox-deactive',
            FindClass: 'sidebox-deactive',
            UploadClass: 'sidebox-deactive',
            ButtonLoadClass: 'sidebox-deactive',
            listStudyKind: ['Общее', 'Профессиональное', 'Дополнительное'],
            listApps:[],
            editApp:[],
            LoadClass: 'vue-active',
            ContentClass: 'vue-deactive',
            sort: '-date_create',
        }
    },
    methods: {
        sorted(obj){
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
                url = this.$store.state.backendUrl+'/api/users/apps?ordering='+this.sort+'&'+this.findString
            } else {
                url = this.$store.state.backendUrl+'/api/users/apps?ordering='+this.sort
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
            this.editApp = await fetch(this.$store.state.backendUrl+'/api/users/app/'+id+'/', {
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
        async editAppFunc(){
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
                    'group': this.$refs.editGroup.value,
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
        uploadSidebox(){
            this.AddClass = 'sidebox-deactive'
            this.ButtonClass = 'sidebox-active'
            this.ButtonLoadClass = 'sidebox-deactive'
            this.EditClass = 'sidebox-deactive'
            this.FindClass = 'sidebox-deactive'
            this.UploadClass = 'sidebox-active'
            this.SideBoxChecked = true
        },
        async uploadApps(){
            this.ButtonClass = 'sidebox-deactive'
            this.ButtonLoadClass = 'sidebox-active'
            if (this.$refs.uploadFile.value.substr(-4) != 'xlsx') {
                showBanner('.banner.error', 'Некорректный формат файла!')
                return false
            }
            var data = new FormData()
            data.append('file', this.$refs.uploadFile.files[0])
            await fetch(this.$store.state.backendUrl+'/api/users/apps_upload/', {
              method: 'PUT',
              headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Authorization': 'Token '+localStorage.getItem('access_token')
              },
              body: data
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.error){
                    showBanner('.banner.error', data.error)
                    this.getApps();
                    this.ButtonClass = 'sidebox-active'
                    this.ButtonLoadClass = 'sidebox-deactive'
                    this.SideBoxChecked = false
                    return false
                } else {
                    showBanner('.banner.success', data.success)
                    this.getApps();
                    this.SideBoxChecked = false
                }
            })
        },
        async downloadApps(){
            await fetch(this.$store.state.backendUrl+'/api/users/apps_download/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie("csrftoken"),
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Authorization': 'Token '+localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    'search': this.findString
                })
            })
            .then((res) => res.blob())
            .then(blob => {
                var file = window.URL.createObjectURL(blob);
                window.location.assign(file);
            })
        }
    },
    created() {
        this.getApps();
    }
 }
</script>

<style>
</style>