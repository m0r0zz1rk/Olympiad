import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
  plugins: [createPersistedState({
    storage: window.localStorage,
  })],
  state: {
    backendUrl: process.env.VUE_APP_BACKEND_URL,
    participant_uuid: localStorage.getItem('participant_uuid') || '',
    token: localStorage.getItem('access_token') || '',
    admin: localStorage.getItem('is_admin') || '',
    status: '',
    participant_next: ''
  },
  getters: {
    getServerUrl: state => state.backendUrl,
    inProgress: state => !!state.participant_uuid,
    isAuthenticated: state => !!state.token,
    isParticipant: state => !!state.participant_uuid,
    authStatus: state => state.status,
  },
  mutations: {
    AUTH_REQUEST (state) {
        state.status = 'loading'
      },
    AUTH_SUCCESS (state, token) {
        state.status = 'success',
        state.token = token
    },
    PARTICIPANT_REQUEST (state) {
        state.status = 'loading'
    },
    PARTICIPANT_SUCCESS (state, {uuid, next}) {
        state.status = 'success'
        state.participant_next = next
        state.participant_uuid = uuid
    },
    START_OLYMP (state) {
        state.participant_next = 'passing'
    },
    STOP_OLYMP (state) {
        state.participant_next = 'sign-in'
    },
    PARTICIPANT_ERROR (state) {
        state.status = 'error'
    },
    AUTH_CHECKADMIN (state, is_admin) {
        state.admin = is_admin
    },
    AUTH_ERROR (state) {
        state.status = 'error'
    },
  },
  actions: {
    AUTH_REQUEST ({commit, dispatch}, user ) {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
          commit('AUTH_REQUEST');
          fetch(this.state.backendUrl+'/api/authen/login/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Content-Type': 'application/json;charset=UTF-8',
            },
            body: JSON.stringify({
                'phone': user.phone_user,
                'pass': user.pass
            })
          })
          .then(resp => resp.json())
          .then(data => {
              if ('error' in data){
                commit('AUTH_ERROR', data.error)
                showBanner('.banner.error', data.error)
              } else {
                const token = data.token
                commit('AUTH_SUCCESS', token)
                localStorage.setItem('access_token', token)
                fetch(this.state.backendUrl+'/api/authen/check_admin/', {
                  method: 'GET',
                  headers: {
                      'Authorization': 'Token '+localStorage.getItem('access_token'),
                  },
                  })
                  .then(res => res.json())
                  .then(data => {
                    if (data.is_admin == true) {
                       localStorage.setItem('is_admin', true)
                       commit('AUTH_CHECKADMIN', true)
                    } else {
                       localStorage.setItem('is_admin', false)
                       commit('AUTH_CHECKADMIN', false)
                    }
                    showBanner('.banner.success', 'Вход выполнен успешно');
                    resolve();
                })
                showBanner('.banner.success', 'Вход выполнен успешно');
                resolve();
              }
            })
          .catch(err => {
            commit('AUTH_ERROR', err)
            localStorage.removeItem('access_token') // if the request fails, remove any possible user token if possible
            localStorage.removeItem('is_admin') // if the request fails, remove any possible user token if possible
            reject(err)
            showBanner('.banner.error', 'Неудачная попытка входа в систему. Поробуйте еще раз')
          })
          })
    },
    AUTH_LOGOUT ({commit, dispatch}) {
        return new Promise((resolve, reject) => {
          localStorage.removeItem('access_token') // clear your user's token from localstorage
          resolve()
        })
    },
    PARTICIPANT_REQUEST ({commit, dispatch}, id ) {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
          commit('PARTICIPANT_REQUEST');
          fetch(this.state.backendUrl+'/api/authen/participant_login/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Content-Type': 'application/json;charset=UTF-8',
            },
            body: JSON.stringify({
                'participant_id': id.id_participant
            })
          })
          .then(resp => {
            if (resp.status == 404) {
                commit('PARTICIPANT_ERROR', 'Участник не найден')
                showBanner('.banner.error', 'Участник не найден')
                return false
            } else {
                return resp.json().then(data => {
                  if ('error' in data){
                    commit('PARTICIPANT_ERROR', data.error)
                    showBanner('.banner.error', data.error)
                  } else if (data.status == 404) {
                    commit('PARTICIPANT_ERROR', 'Участник не найден')
                    showBanner('.banner.error', 'Участник не найден')
                  } else {
                    const uuid = data.uuid
                    const next = data.status
                    commit('PARTICIPANT_SUCCESS', { uuid, next})
                    localStorage.setItem('participant_uuid', uuid)
                    resolve();
                  }
                })
            }
          })
          .catch(err => {
            commit('AUTH_ERROR', err)
            localStorage.removeItem('access_token') // if the request fails, remove any possible user token if possible
            localStorage.removeItem('is_admin') // if the request fails, remove any possible user token if possible
            reject(err)
            showBanner('.banner.error', 'Неудачная попытка входа. Поробуйте еще раз')
          })
        })
    },
    START_OLYMP_REQUEST ({commit, dispatch}) {
        commit('START_OLYMP')
    },
    STOP_OLYMP_REQUEST ({commit, dispatch}) {
        return new Promise((resolve, reject) => {
          localStorage.removeItem('participant_uuid')
          commit('STOP_OLYMP')
          resolve()
        })
    },
  },
  modules: {
  }
})
