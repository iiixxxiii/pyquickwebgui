import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import fs from 'fs';
import path from 'path';

export default defineConfig({
    plugins: [vue(),
        {
            // 钩子,复制到指定目录
            name: 'copy-dist-to-target',
            closeBundle() {
                const sourceDir = path.resolve(__dirname, 'dist'); // 打包输出目录
                const targetDir = path.resolve(__dirname, '../ui'); // 目标目录

                // 检查源目录是否存在
                if (!fs.existsSync(sourceDir)) {
                    console.error(`Source directory "${sourceDir}" does not exist.`);
                    return;
                }

                // 如果目标目录不存在，则创建
                if (!fs.existsSync(targetDir)) {
                    fs.mkdirSync(targetDir, { recursive: true });
                }

                // 复制文件
                copyFolderRecursiveSync(sourceDir, targetDir);

                console.log(`Files copied from "${sourceDir}" to "${targetDir}".`);
            },
        },
    ],
    build: {
        outDir: 'dist', // 打包输出目录
    },
});
// 同步递归复制文件夹
function copyFolderRecursiveSync(source: string, target: string) {
    if (!fs.existsSync(target)) {
        fs.mkdirSync(target);
    }

    // 读取源目录的内容
    const files = fs.readdirSync(source);

    for (const file of files) {
        const sourceFilePath = path.join(source, file);
        const targetFilePath = path.join(target, file);

        // 判断是文件还是目录
        if (fs.lstatSync(sourceFilePath).isDirectory()) {
            copyFolderRecursiveSync(sourceFilePath, targetFilePath); // 递归复制子目录
        } else {
            fs.copyFileSync(sourceFilePath, targetFilePath); // 复制文件
        }
    }
}

// https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })


