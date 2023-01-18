<template>
    <div id="main-content">
        <form class="form-sign" style="width: 70%;" @submit.prevent="registration">
            <div class="table-wrapper">
                <table class="fl-table">
                    <thead>
                        <tr>
                            <th colspan="2">
                                <h4 class="center-text">Регистрация в АИС<br>
                                    <router-link to="/sign-in">
                                        <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                                            type="button">Назад</button>
                                    </router-link>
                                </h4>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Фамилия</td>
                            <td>
                                <input type="text" class="form-control w-75 m-auto text-center" v-model="surname"
                                    id="floatingInput" placeholder="Фамилия" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Имя</td>
                            <td>
                                <input type="text" class="form-control w-75 m-auto text-center" v-model="name"
                                    id="floatingInput" placeholder="Имя" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Отчество</td>
                            <td>
                                <input type="text" class="form-control w-75 m-auto text-center" v-model="patronymic"
                                    id="floatingInput" placeholder="Отчество">
                            </td>
                        </tr>
                        <tr>
                            <td>Полное наименование ОО</td>
                            <td>
                                <textarea class="form-control" v-model="oo_fullname"
                                    placeholder="Полное наименование образовательной организации" required></textarea>
                            </td>
                        </tr>
                        <tr>
                            <td>Физический адрес ОО</td>
                            <td>
                                <textarea class="form-control" v-model="oo_address"
                                    placeholder="Физический адрес образовательной организации" required></textarea>
                            </td>
                        </tr>
                        <tr>
                            <td>Должность</td>
                            <td>
                                <input type="text" class="form-control w-75 m-auto text-center" v-model="position"
                                    id="floatingInput" placeholder="Должность" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>
                                <input type="email" class="form-control w-75 m-auto text-center" v-model="email"
                                    id="floatingInput" placeholder="Адрес электронной почты" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Контактный телефон</td>
                            <td>
                                <input type="text" class="form-control w-75 m-auto text-center" v-model="phone"
                                    id="floatingInput" v-mask="'+7 (###) ###-##-##'"
                                    placeholder="Номер телефона" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Пароль</td>
                            <td>
                                <input type="password" class="form-control w-75 m-auto text-center" v-model="passw"
                                    id="floatingInput" placeholder="Пароль" required>
                            </td>
                        </tr>
                        <tr>
                            <td>Пароль (подтверждение)</td>
                            <td>
                                <input type="password" class="form-control w-75 m-auto text-center" v-model="passw2"
                                    id="floatingInput" placeholder="Пароль" required>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <div v-bind:class="[ButtonClass]" style="margin: 0 auto;">
                                    <button class="btn btn-lg btn-primary m-auto iohk-butt" id="login-button"
                                        type="submit">Регистрация</button>
                                </div>
                                <div v-bind:class="[LoadClass]">
                                    <img src="../assets/gifs/load.gif">
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: "Registration",
    data() {
        return {
            ButtonClass: 'vue-active',
            LoadClass: 'vue-deactive',
            surname: '',
            name: '',
            patronymic: '',
            oo_fullname: '',
            oo_address: '',
            position: '',
            email: '',
            phone: '',
            passw: '',
            passw2: '',
        }
    },
    methods: {
        registration: async function() {
          this.ButtonClass = 'vue-deactive'
          this.LoadClass = 'vue-active'
          await fetch(this.$store.state.backendUrl+'/api/authen/registration/', {
              method: 'POST',
              headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Content-Type': 'application/json;charset=UTF-8',
              },
              body: JSON.stringify({
                'surname': this.surname,
                'name': this.name,
                'patronymic': this.patronymic,
                'oo_fullname': this.oo_fullname,
                'oo_address': this.oo_address,
                'position': this.position,
                'email': this.email,
                'phone': this.phone,
                'passw': this.passw,
                'passw2': this.passw2,
              })
          })
          .then(resp => resp.json())
          .then(data => {
            if (data.error) {
                showBanner('.banner.error', data.error)
                this.ButtonClass = 'vue-active'
                this.LoadClass = 'vue-deactive'
                return false
            } else {
                showBanner('.banner.success', data.success)
                this.$router.push('/sign-in')
            }
          })
        }
    }
}
</script>

<style>
</style>