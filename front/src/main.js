import { createApp } from 'vue'
import VueTheMask from 'vue-the-mask'
import App from './App.vue'
import router from './router'
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {  faUser,
          faDownload,
          faSliders,
          faRightFromBracket,
          faSort,
          faTrash,
          faPlus,
          faMagnifyingGlass,
          faPenToSquare,
          faList,
          faArrowLeft,
          faUpload,
          faSquarePollVertical,
          faBarsProgress,
          faLock,
          faGraduationCap,
          faLayerGroup,
          faCircleQuestion,
          faCopy,
          faEye,
          faCheck,
          faCalculator,
          faTableList,
          faFileExcel} from '@fortawesome/free-solid-svg-icons'

library.add(faUser,
            faDownload,
            faSliders,
            faRightFromBracket,
            faSort,
            faTrash,
            faPlus,
            faMagnifyingGlass,
            faPenToSquare,
            faList,
            faArrowLeft,
            faUpload,
            faSquarePollVertical,
            faBarsProgress,
            faLock,
            faGraduationCap,
            faLayerGroup,
            faCircleQuestion,
            faCopy,
            faEye,
            faCheck,
            faCalculator,
            faTableList,
            faFileExcel)

createApp(App).use(store).use(router).component('font-awesome-icon', FontAwesomeIcon).use(VueTheMask).mount('#app')
