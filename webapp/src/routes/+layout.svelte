<script lang="ts">
  import "../app.pcss";
  import '@fortawesome/fontawesome-free/css/all.css';
  import Navigation from "../lib/navigation/Navigation.svelte";
  import { AppShell, AppBar } from "@skeletonlabs/skeleton";
  import { onMount } from "svelte";
  import { initializeStores, Drawer, getDrawerStore, Modal } from "@skeletonlabs/skeleton";
  import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
  import { storePopup } from '@skeletonlabs/skeleton';
  import { loadStreams, streams } from "../stores/streams";

  initializeStores();
  storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

  const drawerStore = getDrawerStore();
  const title = "Train Whisperer";

  function openDrawer(): void {
    drawerStore.open();
  }

  function closeDrawer(): void {
    drawerStore.close();
  }

  onMount(() => {
    // initialize the stores with data from database
    loadStreams();
  });

</script>

<Modal />
<Drawer width="56" rounded="no">
  <Navigation on:click={closeDrawer} />
</Drawer>
<AppShell slotSidebarLeft="bg-surface-500/5 w-0 lg:w-64">
  <svelte:fragment slot="header">
    <AppBar>
      <svelte:fragment slot="lead">
        <div class="flex items-center">
            <button on:click={openDrawer} class="lg:hidden btn btn-sm mr-4">
                <span>
                    <svg viewBox="0 0 100 80" class="fill-token w-4 h-4">
                        <rect width="100" height="20" />
                        <rect y="30" width="100" height="20" />
                        <rect y="60" width="100" height="20" />
                    </svg>
                </span>
            </button>
          </div>
          <h1><i class="fas fa-train mr-2 text-sm" />{title}</h1>
      </svelte:fragment>
      <svelte:fragment slot="trail">
        <a class="btn-icon hover:variant-soft-primary" href="https://github.com/frillweeman/train-chatter" target="_blank">
          <i class="fa-brands fa-github text-lg"></i>
        </a>
      </svelte:fragment>
    </AppBar>
  </svelte:fragment>
  <svelte:fragment slot="sidebarLeft">
    <Navigation />
  </svelte:fragment>
  <div class="mx-auto max-w-screen-lg">
    <slot />
  </div>
</AppShell>
