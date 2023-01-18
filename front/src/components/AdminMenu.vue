<template>
<nav class="nav__cont">
  <ul class="nav">
    <li class="nav__items ">
      <font-awesome-icon icon="fa-solid fa-user" :style="{ color: white }"/>
      <router-link class="nav-href" to="/admin/users">Пользователи</router-link>
    </li>

    <li class="nav__items ">
      <font-awesome-icon icon="fa-solid fa-list" :style="{ color: white }"/>
       <router-link class="nav-href" to="/admin/apps">Заявки</router-link>
    </li>

    <li class="nav__items ">
      <font-awesome-icon icon="fa-solid fa-graduation-cap" :style="{ color: white }"/>
      <router-link class="nav-href" to="/admin/olympiads">Олимпиады</router-link>
    </li>

    <li class="nav__items ">
      <font-awesome-icon icon="fa-solid fa-square-poll-vertical" :style="{ color: white }"/>
      <router-link class="nav-href" to="/admin/results">Результаты</router-link>
    </li>

  </ul>
</nav>
</template>

<script>
 export default {
    name: "AdminMenu"
 }
</script>

<style>
    .nav__cont {
         position: fixed;
         width: 60px;
         z-index: 100;
         background-color: #00415d;
         overflow: hidden;
         transition: width 0.3s ease;
         cursor: pointer;
         box-shadow: 4px 7px 10px rgba(0, 0, 0, .4);
         border-radius: 25px;
    }
     .nav__cont:hover {
         width: 200px;
    }
     @media screen and (min-width: 600px) {
         .nav__cont {
             width: 45px;
        }
    }
     .nav {
         list-style-type: none;
         color: white;
    }
     .nav:first-child {
         padding-top: 1.5rem;
    }
     .nav__items a {
         position: relative;
         display: block;
         top: -35px;
         padding-left: 25px;
         padding-right: 15px;
         transition: all 0.3s ease;
         margin-left: 25px;
         margin-right: 10px;
         text-decoration: none;
         color: white;
         font-family: Arial;
	     font-weight: bold;
         font-size: 16px;
    }
     .nav__items a:after {
         content: '';
         width: 400%;
         height: 150%;
         position: absolute;
         top: -2px;
         left: -40px;
         border-radius: 2px;
         background: #e85c00;
         opacity: 0;
         transition: all 0.5s ease;
         z-index: -10;
    }
     .nav__items:hover a:after {
         opacity: 1;
    }
     .nav__items svg {
         width: 26px;
         height: 26px;
         position: relative;
         left: -23px;
         cursor: pointer;
    }
     @media screen and (min-width: 600px) {
         .nav__items svg {
             width: 32px;
             height: 32px;
             left: 5px;
        }
    }
</style>