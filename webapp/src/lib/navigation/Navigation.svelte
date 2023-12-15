<script lang="ts">
  import { AppRail, AppRailAnchor } from "@skeletonlabs/skeleton";
  import { page } from "$app/stores";

  const routes = [
    { name: "Live", href: "/live", icon: "tower-broadcast" },
    { name: "Settings", href: "/preferences", icon: "gear" },
  ];

  $: classesActive = (href: string) => ($page.url.pathname.startsWith(href) ? 'bg-primary-active-token' : '');
</script>

<nav class="list-nav p-4">
  <ul>
    {#each routes as route}
      <li>
        <a
          class={classesActive(route.href)}
          href="{route.href}"
          on:click
        >
          <i class={`fas fa-${route.icon} text-lg`}></i>
          <span>{route.name}</span>
        </a>
      </li>
    {/each}
  </ul>
</nav>

<!-- <AppRail>
  {#each routes as route}
    <AppRailAnchor selected={$page.url.pathname.startsWith(route.href)} on:click href="{route.href}">
      <svelte:fragment slot="lead">
        <i class={`fas fa-${route.icon} text-2xl`}></i>
      </svelte:fragment>
      {route.name}
    </AppRailAnchor>
  {/each}
</AppRail> -->
