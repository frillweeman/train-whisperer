<script>
  import "../app.css";
  import NavBar from "./NavBar.svelte";
  import { onDestroy, onMount } from "svelte";

  // let eventSource = null;

  onMount(() =>{
    const theme = localStorage.getItem("theme");
    if (theme) {
      document.documentElement.setAttribute("data-theme", theme);
    }

    // eventSource = new EventSource("http://localhost:8000");
    // eventSource.onmessage = (event) => {
    //   console.log(event);
    // };
  });

  // onDestroy(() => {
  //   eventSource?.close();
  // });
</script>

<NavBar />

<div class="md:container md:mx-auto mt-2 px-2">
  <slot />
</div>
