<template>
    <div class="SignIn">
        <main class="form-signin w-25 m-auto">
            <div class="form-elems-center">
                <img class="mb-4" src="../assets/img/logo.png" style="margin: 0 auto; width: 35%; height: 35%">
                <h1 class="h3 mb-3 fw-normal">АИС Олимпиада</h1>
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button" @click = "participantModal();">Участник</button><br><br>
                <button class="btn btn-lg btn-primary iohk-butt" id="login-button"
                    type="button" @click = "mainModal();">Преподаватель<br>Администратор</button><br><br>
            </div>
        </main>
        <Modal v-show="showModal" @close-modal="showModal = false">
            <template v-slot:main-info>
                <div v-bind:class="[ParticipantLogin, 'contain']">
                    <form class="form-sign" @submit.prevent="login_participant">
                        <div class="form-elems-center">
                            <h3 class="h3 mb-3 fw-normal">Введите идентификатор участника</h3>
                            <div class="form-floating">
                              <input type="text" class="form-control w-75 m-auto" v-mask="'#####-#####'"
                                v-model="id_participant" id="floatingInput" placeholder="Идентификатор">
                            </div><br>
                            <button class="w-50 btn btn-lg btn-primary iohk-butt" id="login-button"
                                type="submit">Войти</button>
                        </div>
                    </form>
                </div>
                <div v-bind:class="[MainLogin]">
                    <form class="form-sign" @submit.prevent="login_user">
                        <div class="form-elems-center">
                            <h3 class="h3 mb-3 fw-normal">Вход в систему</h3>
                            <div class="form-floating">
                              <input type="text" class="form-control w-75 m-auto" v-model="phone_user"
                                id="floatingInput" v-mask="'+7 (###) ###-##-##'" placeholder="Телефон">
                            </div>
                            <div class="form-floating">
                              <input type="password" class="form-control w-75 m-auto" v-model="pass"
                                id="floatingPassword" placeholder="Пароль">
                            </div><br>
                            <button class="w-50 btn btn-lg btn-primary iohk-butt" id="login-button"
                                type="submit">Войти</button><br><br>
                            <router-link to="/registration">
                                <button class="w-50 btn btn-lg btn-primary iohk-butt" id="login-button"
                                    type="button">Регистрация</button>
                            </router-link>
                        </div>
                    </form>
                </div>
           </template>
           <template v-slot:load>
                <div v-bind:class="[Load]">
                    <img class="mb-4" src="../assets/gifs/load.gif">
                </div>
           </template>
        </Modal>
    </div>
</template>

<script>

import Modal from '../components/Modal.vue'

export default {
    components:{
        Modal
    },
    data() {
        return {
            ParticipantLogin: 'modal-deactive',
            MainLogin: 'modal-deactive',
            Load: 'load-hide',
            showModal: false,
        }
    },
    methods:{
        login_participant: function() {
          this.ParticipantLogin = 'modal-deactive'
          this.Load = 'load-show'
          const { id_participant } = this;
          if (id_participant == null) {
            showBanner('.banner.error', 'Введите идентификатор участника')
            this.ParticipantLogin = 'modal-active'
            this.Load = 'load-hide'
            return false
          }
          this.$store.dispatch('PARTICIPANT_REQUEST', { id_participant }).then(() => {
             if (this.$store.state.participant_next == 'passing') {
                this.$router.push('/olympic')
             } else {
                this.$router.push('/start')
             }
          })
          this.ParticipantLogin = 'modal-active'
          this.Load = 'load-hide'
        },
        login_user: function() {
          this.MainLogin = 'modal-deactive'
          this.Load = 'load-show'
          const { phone_user, pass } = this;
          this.$store.dispatch('AUTH_REQUEST', { phone_user, pass }).then(() => {
             if (getUrlParameter('nextUrl')) {
                this.$router.push({ path: getUrlParameter('nextUrl') })
             } else this.$router.push('/')
          })
          this.MainLogin = 'modal-active'
          this.Load = 'load-hide'
        },
        participantModal(){
            this.showModal = true
            this.ParticipantLogin = 'modal-active'
            this.MainLogin = 'modal-deactive'
            this.Load = 'load-hide'
        },
        mainModal(){
            this.showModal = true
            this.ParticipantLogin = 'modal-deactive'
            this.MainLogin = 'modal-active'
            this.Load = 'load-hide'
        },
    }
}
</script>

<style>
.modal-active, .load-show {
  display: block;
  visibility: visible;
  pointer-events: auto;
}
.modal-deactive, .load-hide {
  display: none;
  visibility: collapse;
  pointer-events: none;
}
.contain{
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  position: absolute;
}
.SignIn{
    color: #00415d;
    width: 100vw;
    height: 100vh;
    display: flex;
    vertical-align: middle;
}
.form-elems-center{
    text-align:center;
    align-items:center;
    justify-content: center;
    vertical-align: middle;
}
.iohk-butt{
    background-color: #00415d;
    border-color: #00415d;
}
.iohk-butt:hover{
    background-color: #e85c00;
    border-color: #e85c00;
}

.form-control::-webkit-input-placeholder { color: #00415d !important}  /* WebKit, Blink, Edge */
.form-control:-moz-placeholder { color: #00415d; }  /* Mozilla Firefox 4 to 18 */
.form-control::-moz-placeholder { color: #00415d; }  /* Mozilla Firefox 19+ */
.form-control:-ms-input-placeholder { color: #00415d; }  /* Internet Explorer 10-11 */
.form-control::-ms-input-placeholder { color: #00415d; }  /* Microsoft Edge */


@import '~bootstrap';
</style>
