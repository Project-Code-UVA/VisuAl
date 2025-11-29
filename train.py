if __name__ == "__main__":
    # train.py
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torchvision import datasets
    from torch.utils.data import DataLoader, Subset
    import numpy as np
    from model import DenseNetCustom, transform, device

    # ----------------------------
    # Dataset paths
    # ----------------------------
    train_dir = r"C:\Users\julia\VisuAl\140k_realfake_faces_dataset\train"  # replace with your path
    val_dir = r"C:\Users\julia\VisuAl\140k_realfake_faces_dataset\valid"      # replace with your path

    # ----------------------------
    # Load datasets
    # ----------------------------
    full_train_dataset = datasets.ImageFolder(train_dir, transform=transform)
    full_val_dataset = datasets.ImageFolder(val_dir, transform=transform)

    # ----------------------------
    # Take a small random subset (e.g., 1000 images)
    # ----------------------------
    N_train = 1000
    train_indices = np.random.choice(len(full_train_dataset), N_train, replace=False)
    train_dataset = Subset(full_train_dataset, train_indices)

    N_val = min(200, len(full_val_dataset))  # small validation subset
    val_indices = np.random.choice(len(full_val_dataset), N_val, replace=False)
    val_dataset = Subset(full_val_dataset, val_indices)

    # ----------------------------
    # DataLoaders
    # ----------------------------
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)

    # ----------------------------
    # Model, loss, optimizer
    # ----------------------------
    model = DenseNetCustom(num_classes=2).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    # ----------------------------
    # Training loop
    # ----------------------------
    num_epochs = 5  # small number for testing
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0
        correct = 0
        total = 0

        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_acc = correct / total
        train_loss = running_loss / len(train_loader)

        # ----------------------------
        # Evaluate on small validation set
        # ----------------------------
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)
        val_acc = val_correct / val_total

        print(f"Epoch {epoch+1}/{num_epochs} | "
            f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
            f"Val Acc: {val_acc:.4f}")

    # ----------------------------
    # Save model
    # ----------------------------
    torch.save(model.state_dict(), "densenet_fake_detector_small.pth")
    print("Training complete. Model saved as densenet_fake_detector_small.pth")
