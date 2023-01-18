<template>
  <Header/>
  <div id="main-content">
    <div id="cont">
        <h2>Добро пожаловать!</h2><br>
        Для навигации по АИС вопспользуйтесь меню, находящемся в правом верхнем углу.<br>
        <b>Расписание ближайших олимпиад:</b><br>
        <div class="container-table">
            <div class="table-wrapper">
                <table class="fl-table">
                    <thead>
                        <tr>
                            <th>Дата проведения</th>
                            <th>Тема</th>
                            <th>Сроки подачи заявок</th>
                            <th>Время прохождения олимпиады<br></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="olympiad in listOlympiads">
                            <td class="no-wrap">
                                {{ olympiad.event_date }}
                            </td>
                            <td>{{ olympiad.theme }} </td>
                            <td class="no-wrap">
                                {{ olympiad.date_reg_start }} - {{ olympiad.date_reg_end }}
                            </td>
                            <td class="no-wrap">{{ olympiad.time_complete }} мин.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import Header from "../components/Header.vue"

export default {
  name: 'Main',
  components: {Header},
  data() {
    return {
        listOlympiads: []
    }
  },
  methods: {
    async getOlympiads() {
        this.listOlympiads = await fetch(this.$store.state.backendUrl+'/api/authen/mainpage_olympiads/', {
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
    }
  },
  created() {
    this.getOlympiads()
  }
}
</script>

<style>
  #cont{
   color: #00415d;
   width: 75%;
   height: 75%;
   margin: 0 auto;
  }
</style>
