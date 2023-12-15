<script>
  import { page } from "$app/stores";

  const routes = [
    { name: "Live", href: "/live"},
    { name: "Settings", href: "/settings" },
  ];

  let menuOpen = false;
</script>


<div class="navbar bg-base-100 shadow-md sticky" style="z-index: 9999">
  <div class="flex-1">
    <a href="/" class="btn btn-ghost text-xl">Train Whisperer</a>
  </div>

  <!-- Desktop -->
  <div class="flex-none hidden md:flex">
    <ul class="menu menu-horizontal px-1 font-medium">
      {#each routes as route}
        <li class="text-center mx-1"><a class:selected={$page.url.pathname.startsWith(route.href)} href={route.href}>{route.name}</a></li>
      {/each}
    </ul>
  </div>

  <!-- Mobile -->
  <div class="flex-none md:hidden">
    <details class="menu" open={menuOpen}>
      <summary on:click|preventDefault={() => menuOpen = !menuOpen} class="btn btn-ghost btn-sm">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </summary>
      <ul class="menu-dropdown p-2 shadow-lg bg-base-100 rounded-box w-52 absolute right-0">
        {#each routes as route}
          <li on:click={() => menuOpen = false} class="text-center"><a class:selected={$page.url.pathname.startsWith(route.href)} href={route.href}>{route.name}</a></li>
        {/each}
      </ul>
    </details>
  </div>

</div>

<style lang="postcss">
  .selected {
    @apply bg-slate-700 text-slate-50;
  }
</style>
