import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index.js'

import Main from "../views/Main.vue"
import Sign from "../views/Sign.vue"
import Profile from "../views/Profile.vue"
import Registration from "../views/Registration.vue"

import Apps from "../views/users/Apps.vue"

import Users from "../views/admins/administrative/Users.vue"
import AdminApps from "../views/admins/administrative/Apps.vue"
import Olympiads from "../views/admins/administrative/Olympiads.vue"
import OlympiadLevels from "../views/admins/administrative/OlympiadLevels.vue"
import Results from "../views/admins/administrative/Results.vue"
import ResultsCompletes from "../views/admins/administrative/ResultsCompletes.vue"
import ResultDetail from "../views/admins/administrative/ResultDetail.vue"

import QuestionLevels from "../views/admins/tests/QuestionLevels.vue"
import Questions from "../views/admins/tests/Questions.vue"
import NewQuestion from "../views/admins/tests/NewQuestion.vue"
import EditQuestion from "../views/admins/tests/EditQuestion.vue"

import Answers from "../views/admins/tests/Answers.vue"

import StartPage from "../views/participants/StartPage.vue"
import Olympic from "../views/participants/Olympic.vue"


const ifAuthenticated = (to, from, next) => {
  if (!(store.getters.isAuthenticated)) {
    showBanner('.banner.error', 'Пожалуйста, ввойдите в систему')
    next('/sign-in?nextUrl='+to.path)
    return
  } else {
    fetch(store.state.backendUrl+'/api/authen/check_auth/', {
      method: 'GET',
      headers: {
          'Authorization': 'Token '+localStorage.getItem('access_token'),
      },
    })
    .then(resp => {
      if (resp.status == 401 || resp.status == 403) {
        next('/sign-in?nextUrl='+to.path)
        return
      } else {
        next()
        return
      }
    })
  }
}

const ifParticipantStart = (to, from, next) => {
  if (!(store.getters.isParticipant)) {
    showBanner('.banner.error', 'Пожалуйста, введите идентификатор участника, нажав на кнопку "Участник"')
    next('/sign-in')
    return
  } else {
    next();
  }
}

const ifParticipantOlympic = (to, from, next) => {
  if (!(store.getters.isParticipant)) {
    showBanner('.banner.error', 'Пожалуйста, введите идентификатор участника, нажав на кнопку "Участник"')
    next('/sign-in')
    return
  } else if (store.state.participant_next == 'sign-in'){
    next('/sign-in')
    return
  } else if (store.state.participant_next == 'start'){
    next('/start')
    return
  } else {
    next();
  }
}

const isAdministrator = (to, from, next) => {
    if (store.state.admin == true) {
        next()
        return
    } else {
        showBanner('.banner.error', 'У вас нет доступа на просмотр данного раздела')
        next('/')
        return
    }
}

const isUser = (to, from, next) => {
    if ((store.state.admin == false) && (store.state.id_participant == null)) {
        next()
        return
    } else {
        showBanner('.banner.error', 'У вас нет доступа на просмотр данного раздела')
        next('/')
        return
    }
}

const routes = [
  {
    path: '/sign-in',
    name: 'SignIn',
    component: Sign,
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration,
  },
  {
    path: '/',
    name: 'Main',
    component: Main,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/apps',
    name: 'Apps',
    component: Apps,
    beforeEnter: [ifAuthenticated, isUser]
  },
  {
    path: '/admin/users',
    name: 'Users',
    component: Users,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/apps',
    name: 'AdminApps',
    component: AdminApps,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/olympiads',
    name: 'Olympiads',
    component: Olympiads,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/results',
    name: 'Results',
    component: Results,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/results/participants',
    name: 'ResultsCompletes',
    component: ResultsCompletes,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/result_detail/',
    name: 'ResultDetail',
    component: ResultDetail,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/olympiad_levels',
    name: 'OlympiadLevels',
    component: OlympiadLevels,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/question_levels',
    name: 'QuestionLevels',
    component: QuestionLevels,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/questions',
    name: 'Questions',
    component: Questions,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/new_question',
    name: 'NewQuestion',
    component: NewQuestion,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/edit_question',
    name: 'EditQuestion',
    component: EditQuestion,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/admin/answers',
    name: 'Answers',
    component: Answers,
    beforeEnter: [ifAuthenticated, isAdministrator]
  },
  {
    path: '/start',
    name: 'StartPage',
    component: StartPage,
    beforeEnter: ifParticipantStart
  },
  {
    path: '/olympic',
    name: 'Olympic',
    component: Olympic,
    beforeEnter: ifParticipantOlympic
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
