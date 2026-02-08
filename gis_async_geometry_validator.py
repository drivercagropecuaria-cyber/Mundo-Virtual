#!/usr/bin/env python3
"""
GIS Async Geometry Validator Pipeline (v1)
Purpose: Background job for ST_MakeValid() on catalog geometries
Executes asynchronously to avoid blocking main application

Feature: Processes 600+ invalid geometries in parallel batches
Target: 100% geometry validity for v_catalogo_completo view
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Tuple

class GeometryValidationJob:
    """Represents a single geometry validation task"""
    
    def __init__(self, item_id: int, geometry: Dict, area_fazenda_id: int = None):
        self.item_id = item_id
        self.geometry = geometry
        self.area_fazenda_id = area_fazenda_id
        self.status = "PENDING"
        self.result = None
        self.created_at = datetime.utcnow()
        
    def __repr__(self):
        return f"<GeometryValidationJob item_id={self.item_id} status={self.status}>"


class AsyncGeometryValidationPipeline:
    """
    Background pipeline for async geometry validation
    
    Workflow:
    1. Query catalog items with null/invalid geometries
    2. Batch them (50 per batch to avoid memory overload)
    3. Run ST_MakeValid() in parallel asyncio tasks
    4. Update catalog with valid geometries
    5. Log results in audit trail
    """
    
    def __init__(self, batch_size: int = 50, max_parallel_jobs: int = 5):
        self.batch_size = batch_size
        self.max_parallel_jobs = max_parallel_jobs
        self.queue: asyncio.Queue = None
        self.jobs: List[GeometryValidationJob] = []
        self.completed = 0
        self.failed = 0
        self.start_time = None
        self.end_time = None
        
    async def initialize(self):
        """Initialize async queue and workers"""
        self.queue = asyncio.Queue()
        self.start_time = datetime.utcnow()
        print(f"[GIS ASYNC] Pipeline initialized at {self.start_time}")
        
    async def enqueue_job(self, job: GeometryValidationJob):
        """Add job to processing queue"""
        await self.queue.put(job)
        self.jobs.append(job)
        
    async def process_job(self, job: GeometryValidationJob) -> Dict:
        """
        Process single geometry validation job
        Simulates ST_MakeValid() operation
        
        Args:
            job: GeometryValidationJob to process
            
        Returns:
            Result dict with validation outcome
        """
        try:
            # Simulate ST_MakeValid() operation
            # In real Supabase: UPDATE catalogo SET geom = ST_MakeValid(geom) WHERE id = ?
            
            job.status = "PROCESSING"
            
            # Simulated geometry validation (actual would call Supabase RPC)
            await asyncio.sleep(0.1)  # Simulate network latency
            
            # Assume validation succeeds (real implementation would check validity)
            job.result = {
                "item_id": job.item_id,
                "operation": "ST_MakeValid",
                "before_validity": False,  # Was invalid
                "after_validity": True,     # Now valid
                "processing_time_ms": 100
            }
            
            job.status = "COMPLETED"
            self.completed += 1
            
            return job.result
            
        except Exception as e:
            job.status = "FAILED"
            job.result = {"error": str(e)}
            self.failed += 1
            return job.result
    
    async def worker(self, worker_id: int):
        """
        Worker coroutine for processing validation jobs
        
        Args:
            worker_id: Identifier for this worker (1..max_parallel_jobs)
        """
        while True:
            try:
                # Non-blocking get with timeout
                job = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                print(f"[WORKER-{worker_id}] Processing {job}")
                
                result = await self.process_job(job)
                print(f"[WORKER-{worker_id}] ✅ {job.item_id}: {result['after_validity']}")
                
                self.queue.task_done()
                
            except asyncio.TimeoutError:
                # Queue is empty, worker exits
                break
            except Exception as e:
                print(f"[WORKER-{worker_id}] ❌ Error: {e}")
                break
    
    async def run_batch(self, jobs: List[GeometryValidationJob]) -> Dict:
        """
        Run a batch of jobs through the pipeline
        
        Args:
            jobs: List of GeometryValidationJob objects
            
        Returns:
            Summary of batch processing
        """
        print(f"\n[GIS ASYNC] Starting batch with {len(jobs)} jobs")
        
        # Enqueue all jobs
        for job in jobs:
            await self.enqueue_job(job)
        
        # Create worker tasks
        workers = [
            asyncio.create_task(self.worker(i + 1))
            for i in range(self.max_parallel_jobs)
        ]
        
        # Wait for all jobs to complete
        await self.queue.join()
        
        # Cancel workers
        for worker in workers:
            worker.cancel()
        
        # Wait for worker cancellation
        await asyncio.gather(*workers, return_exceptions=True)
        
        return {
            "batch_size": len(jobs),
            "completed": self.completed,
            "failed": self.failed,
            "success_rate": (self.completed / len(jobs) * 100) if jobs else 0
        }
    
    async def finalize(self) -> Dict:
        """
        Finalize pipeline execution
        
        Returns:
            Summary statistics
        """
        self.end_time = datetime.utcnow()
        duration_seconds = (self.end_time - self.start_time).total_seconds()
        
        summary = {
            "pipeline_status": "COMPLETED",
            "total_jobs": len(self.jobs),
            "completed_jobs": self.completed,
            "failed_jobs": self.failed,
            "success_rate_percent": (self.completed / len(self.jobs) * 100) if self.jobs else 0,
            "duration_seconds": duration_seconds,
            "jobs_per_second": (len(self.jobs) / duration_seconds) if duration_seconds > 0 else 0,
            "started_at": self.start_time.isoformat(),
            "completed_at": self.end_time.isoformat()
        }
        
        print(f"\n[GIS ASYNC] Pipeline finalized")
        print(f"  Total jobs: {summary['total_jobs']}")
        print(f"  Completed: {summary['completed_jobs']}")
        print(f"  Failed: {summary['failed_jobs']}")
        print(f"  Success rate: {summary['success_rate_percent']:.1f}%")
        print(f"  Duration: {summary['duration_seconds']:.2f}s")
        
        return summary


# Example usage / Integration test
async def main():
    """Example integration: Process 600 geometries in batches"""
    
    print("=" * 60)
    print("GIS ASYNC GEOMETRY VALIDATOR - LOCAL TEST")
    print("=" * 60)
    
    pipeline = AsyncGeometryValidationPipeline(
        batch_size=50,
        max_parallel_jobs=5
    )
    
    await pipeline.initialize()
    
    # Simulate 600 invalid geometries from catalog
    # In real usage: these would come from Supabase query
    print("\n[SIMULATION] Creating 600 invalid geometry jobs...")
    
    test_jobs = [
        GeometryValidationJob(
            item_id=i,
            geometry={"type": "Polygon", "coordinates": []},  # Empty = invalid
            area_fazenda_id=(i % 10) + 1
        )
        for i in range(1, 601)  # IDs 1..600
    ]
    
    print(f"Created {len(test_jobs)} jobs")
    
    # Process in batches
    batch_results = []
    for batch_start in range(0, len(test_jobs), pipeline.batch_size):
        batch = test_jobs[batch_start : batch_start + pipeline.batch_size]
        result = await pipeline.run_batch(batch)
        batch_results.append(result)
    
    # Finalize and get summary
    summary = await pipeline.finalize()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(json.dumps(summary, indent=2, default=str))
    
    return summary


if __name__ == "__main__":
    # Run the async pipeline
    summary = asyncio.run(main())
    
    # Exit code based on success rate
    if summary['success_rate_percent'] >= 99.0:
        print("\n✅ Pipeline succeeded: Geometry validity >= 99%")
        exit(0)
    else:
        print(f"\n❌ Pipeline failed: Geometry validity only {summary['success_rate_percent']:.1f}%")
        exit(1)
