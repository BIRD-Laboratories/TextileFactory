#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    float x, y;
} Vec2;

typedef struct {
    Vec2 position;
    Vec2 velocity;
    char type[4];
    int area;
    time_t start_time;
    float path_progress;
    int path_index;
} Material;

typedef struct {
    int width, height;
    Material *materials;
    int material_count;
    float distance_threshold;
    float time_threshold;
    float item_rate;
    float steps_per_second;
    Vec2 *conveyor_paths;
    int conveyor_path_count;
} Physics2D;

Physics2D* create_physics2d(int width, int height, float distance_threshold, float time_threshold, float item_rate, float steps_per_second, Vec2 *conveyor_paths, int conveyor_path_count) {
    Physics2D *physics = (Physics2D*)malloc(sizeof(Physics2D));
    physics->width = width;
    physics->height = height;
    physics->materials = NULL;
    physics->material_count = 0;
    physics->distance_threshold = distance_threshold;
    physics->time_threshold = time_threshold;
    physics->item_rate = item_rate;
    physics->steps_per_second = steps_per_second;
    physics->conveyor_paths = conveyor_paths;
    physics->conveyor_path_count = conveyor_path_count;
    return physics;
}

void spawn_material(Physics2D *physics, Vec2 pos, const char *material_type) {
    physics->material_count++;
    physics->materials = (Material*)realloc(physics->materials, physics->material_count * sizeof(Material));
    Material *material = &physics->materials[physics->material_count - 1];
    material->position = pos;
    material->velocity.x = 0.0;
    material->velocity.y = 0.0;
    strncpy(material->type, material_type, 3);
    material->type[3] = '\0';
    material->area = 0;
    material->start_time = time(NULL);
    material->path_progress = 0.0;
    material->path_index = 0;
}

void vectorized_move_materials(Physics2D *physics, float speed) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        material->path_progress += speed;
        if (material->path_progress >= 1.0) {
            material->path_index++;
            material->path_progress = 0.0;
        }
        material->path_index %= physics->conveyor_path_count;

        Vec2 start_pos = physics->conveyor_paths[material->path_index];
        Vec2 end_pos = physics->conveyor_paths[(material->path_index + 1) % physics->conveyor_path_count];
        float t = material->path_progress;

        material->position.x = start_pos.x + t * (end_pos.x - start_pos.x);
        material->position.y = start_pos.y + t * (end_pos.y - start_pos.y);
    }
}

void update(Physics2D *physics, float dt) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        material->position.x += material->velocity.x * dt;
        material->position.y += material->velocity.y * dt;
    }
}

void get_state_array(Physics2D *physics, int **state_array) {
    for (int i = 0; i < physics->material_count; i++) {
        Material *material = &physics->materials[i];
        int x = (int)material->position.x;
        int y = (int)material->position.y;
        if (0 <= x && x < physics->width && 0 <= y && y < physics->height) {
            if (strcmp(material->type, "Cot") == 0) {
                state_array[x][y] = 1;
            } else if (strcmp(material->type, "Fab") == 0) {
                state_array[x][y] = 2;
            } else if (strcmp(material->type, "Fin") == 0) {
                state_array[x][y] = 3;
            }
        }
    }
}

void print_state_array(Physics2D *physics, int **state_array) {
    for (int y = 0; y < physics->height; y++) {
        for (int x = 0; x < physics->width; x++) {
            printf("%d ", state_array[x][y]);
        }
        printf("\n");
    }
}

void free_physics2d(Physics2D *physics) {
    free(physics->materials);
    free(physics);
}
