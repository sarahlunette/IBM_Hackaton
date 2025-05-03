class ResourceDispatcher:
    def __init__(self, allocation: dict):
        self.allocation = allocation

    def dispatch_resources(self):
        print("Dispatching Resources:")
        for resource, count in self.allocation.items():
            print(f" - {count} units of {resource} sent.")
