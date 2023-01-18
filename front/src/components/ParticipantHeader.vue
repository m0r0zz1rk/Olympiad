<template>
    <div class="container-nav">
        <div class="content-nav">
            <div class="inl-block-nav">
                <img src="../assets/img/150x150.png" style="width:50px; height:50px;">
            </div>
            <div class="inl-block-nav">
                <b class="nav-text">ГБПОУ ИОХК</b>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name: "ParticipantHeader"
    }
</script>

<style>
    a.nav-href,
    a.nav-href:hover,
    a.nav-href:active{
     color: white;
     text-decoration: none;
    }
    .inl-block-nav{
     margin-left: 10px;
     display: inline-block;
    }
    .nav-text{
     font-size: 18px;
	 font-weight: bold;
	 color: #00415d;
    }
    .container-nav{
     position: relative;
     top: 10px;
     width: 100%;
     align-content: center;
     justify-content: center;
     margin-bottom: 50px;
    }
    .content-nav{
        width: 100%;
        margin: 0 auto;
    }
    .menu-bar {
     border-radius: 25px;
     height: fit-content;
     display: inline-flex;
     background-color: #00415d;
     -webkit-backdrop-filter: blur(10px);
     backdrop-filter: blur(10px);
     align-items: center;
     padding: 0 10px;
    }
    .menu-bar li {
	 list-style: none;
	 color: white;
	 font-family: Arial;
	 font-weight: bold;
	 padding: 12px 16px;
	 margin: 0 8px;
	 position: relative;
	 cursor: pointer;
	 white-space: nowrap;
    }
    .menu-bar li::before {
	 content: " ";
	 position: absolute;
	 top: 0;
	 left: 0;
	 height: 100%;
	 width: 100%;
	 z-index: -1;
	 transition: 0.2s;
	 border-radius: 25px;
    }
    .menu-bar li:hover::before {
	 background: linear-gradient(to bottom, #e85c00, #e85c00);
	 box-shadow: 0px 3px 20px 0px black;
	 transform: scale(1.2);
    }
</style>